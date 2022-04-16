import os
from dotenv import load_dotenv

# load env variables
is_heroku = os.getenv("IS_HEROKU", None)
if not is_heroku:
    load_dotenv()

discord_log_webhook = os.getenv("LOG_WEBHOOK")
discord_spirits_webhook = os.getenv("SPIRITS_WEBHOOK")

nft_contract = "0x38eeF32ae1978bD4240605F5d3f98A4427fdC845"
nft_subgraph_url = "https://api.thegraph.com/subgraphs/name/tomfutago/forest-spirits"
eth_blocks_subgraph_url = "https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks"
