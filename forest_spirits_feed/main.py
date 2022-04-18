import os
import shutil
import requests
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
from forest_spirits_feed.graphql import *


def download_thumb(url: str, thumb_path: str):
    if url.startswith("ipfs://"):
        url = url.replace("ipfs://", "https://ipfs.io/ipfs/")
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        with open(thumb_path, "wb") as f:
            shutil.copyfileobj(res.raw, f)


# init blocks
block_latest = 0
block_current = 0

while True:
    try:
        # get latest block
        block_latest = getEthBlockLatest()
        if block_current >= block_latest:
            #sleep(1)
            continue
        else:
            block_current = block_latest
        
        # check if sale event valid
        saleEvent = getSaleEventPerBlock(block_current)
        if saleEvent[0]["isSale"] == False:
            continue
        
        # loop through each sale event (in most cases it will be only 1)
        for n in range(len(saleEvent)):
            spirit = getForestSpiritPerId(saleEvent[n]["tokenId"])
            if spirit["isForestSpirit"] == False:
                continue

            # collect discord output
            title = "Forest Spirit sold!"
            opensea = "https://opensea.io/assets/" + config.nft_contract + "/" + str(spirit["tokenId"])
            looksrare = "https://looksrare.org/collections/" + config.nft_contract + "/" + str(spirit["tokenId"])
            #content = spirit["name"] + " sold for " + f'{int(saleEvent[n]["amount"]) / 10 ** 18 :.2f} ETH'
            
            info = "**" + spirit["name"] + "**"
            info += "\n"
            info += "\nPrice: " + f'{int(saleEvent[n]["amount"]) / 10 ** 18 :.2f} ETH'
            info += "\nBuyer: " + saleEvent[n]["to"][:8] + ".." + saleEvent[n]["to"][34:]
            info += "\nSeller: " + saleEvent[n]["from"][:8] + ".." + saleEvent[n]["from"][34:]
            info += "\n"
            info += "\n*Ancestor:* **" + spirit["ancestor"] + "** | *Body:* **" + spirit["body"]
            info += "** | *Element:* **" + spirit["element"] + "** | *Environment:* **" + spirit["environment"]
            info += "** | *Mask:* **" + spirit["mask"] + "** | *Origin:* **" + spirit["origin"]
            info += "** | *Pedestal:* **" + spirit["pedestal"] + "** | *Staff:* **" + spirit["staff"] + "**"
            info += "\n"
            info += "\n[Opensea](" + opensea + ") | [LooksRare](" + looksrare + ")"

            color = "FDFEFE" #white
            image_url = spirit["image_url"]
            footer = "Sold on "
            timestamp = saleEvent[n]["timestamp"]

            webhook = DiscordWebhook(url=config.discord_spirits_webhook, rate_limit_retry=True)
            
            file_name = spirit["name"] + " sold for " + f'{int(saleEvent[n]["amount"]) / 10 ** 18 :.2f} ETH.png'
            file_name = str(file_name).replace("#", "").replace(" ", "_")
            thumb_path = "./" + file_name
            
            download_thumb(image_url, thumb_path)
            with open(thumb_path, "rb") as f:
                webhook.add_file(file=f.read(), filename=file_name)
            token_url = "attachment://" + file_name

            embed = DiscordEmbed(title=title, color=color)
            embed.set_description(info)
            embed.set_thumbnail(url=token_url)
            embed.set_footer(text=footer)
            embed.set_timestamp(timestamp)
            webhook.add_embed(embed)
            response = webhook.execute()

            try:
                os.remove(thumb_path)
            except:
                continue
        
    except:
        continue
