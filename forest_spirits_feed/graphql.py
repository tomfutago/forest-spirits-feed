import json
import requests
from forest_spirits_feed import config

def sendQuery(query: str, url: str) -> json:
    r = requests.post(url, json={"query": query})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return json.loads('{"data": "error"}')

def getEthBlockLatest() -> int:
    query = """query {
    blocks(first: 1, skip: 5, orderBy: number, orderDirection: desc) {
        number
        timestamp
        }
    }
    """
    json_data = sendQuery(query=query, url=config.eth_blocks_subgraph_url)
    return int(json_data["data"]["blocks"][0]["number"])

def getSaleEventLatest() -> list[dict]:
    query = """query {
    saleEvents(first: 1, orderBy: block, orderDirection: desc) {
        id
        idx
        nft {
            id
        }
        from {
            id
        }
        to {
            id
        }
        amount
        block
        hash
        timestamp
        }
    }
    """
    json_data = sendQuery(query=query, url=config.nft_subgraph_url)

    output = []
    if "error" in str(json_data):
        return [{"isSale": False}]
    else:
        for sale in json_data["data"]["saleEvents"]:
            if "id" not in str(sale):
                output.append({"isSale": False})
            else:
                output.append({
                    "isSale": True,
                    "tokenId": int(sale["nft"]["id"]),
                    "from": str(sale["from"]["id"]),
                    "to": str(sale["to"]["id"]),
                    "amount": int(sale["amount"]),
                    "block": int(sale["block"]),
                    "hash": str(sale["hash"]),
                    "timestamp": int(sale["timestamp"])
                })
    return output

def getSaleEventPerBlock(block: int) -> list[dict]:
    query = """query {
    saleEvents(where: {
        block: %i
    }) {
        id
        idx
        nft {
            id
        }
        from {
            id
        }
        to {
            id
        }
        amount
        block
        hash
        timestamp
        }
    }
    """ % (block)
    json_data = sendQuery(query=query, url=config.nft_subgraph_url)
    
    output = []
    if "error" in str(json_data):
        return [{"isSale": False}]
    else:
        for sale in json_data["data"]["saleEvents"]:
            if "id" not in str(sale):
                output.append({"isSale": False})
            else:
                output.append({
                    "isSale": True,
                    "tokenId": int(sale["nft"]["id"]),
                    "from": str(sale["from"]["id"]),
                    "to": str(sale["to"]["id"]),
                    "amount": int(sale["amount"]),
                    "block": int(sale["block"]),
                    "hash": str(sale["hash"]),
                    "timestamp": int(sale["timestamp"])
                })
    return output

def getForestSpiritPerId(id: int) -> dict:
    query = """query {
    forestSpirit(id: "%i") {
        tokenID
        name
        image
        animation_url
        body
        mask
        staff
        element
        pedestal
        environment
        ancestor
        origin
        }
    }
    """ % (id)
    json_data = sendQuery(query=query, url=config.nft_subgraph_url)
    
    if "error" in str(json_data):
        return {"isForestSpirit": False}
    elif "tokenID" not in str(json_data):
        return {"isForestSpirit": False}
    else:
        return {
            "isForestSpirit": True,
            "tokenId": int(json_data["data"]["forestSpirit"]["tokenID"]),
            "name": str(json_data["data"]["forestSpirit"]["name"]),
            "image_url": str(json_data["data"]["forestSpirit"]["image"]),
            "animation_url": str(json_data["data"]["forestSpirit"]["animation_url"]),
            "body": str(json_data["data"]["forestSpirit"]["body"]),
            "mask": str(json_data["data"]["forestSpirit"]["mask"]),
            "staff": str(json_data["data"]["forestSpirit"]["staff"]),
            "element": str(json_data["data"]["forestSpirit"]["element"]),
            "pedestal": str(json_data["data"]["forestSpirit"]["pedestal"]),
            "environment": str(json_data["data"]["forestSpirit"]["environment"]),
            "ancestor": str(json_data["data"]["forestSpirit"]["ancestor"]),
            "origin": str(json_data["data"]["forestSpirit"]["origin"])
        }
