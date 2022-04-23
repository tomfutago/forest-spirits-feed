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
        _meta {
            block {
            number
            }
        }
    }
    """
    json_data = sendQuery(query=query, url=config.nft_subgraph_url)
    return int(json_data["data"]["_meta"]["block"]["number"])

def getSaleEventLatest() -> list[dict]:
    query = """query {
    saleEvents(first: 1, orderBy: block, orderDirection: desc) {
        id
        idx
        nft {
            tokenID
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
                    "tokenId": int(sale["nft"]["tokenID"]),
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
            tokenID
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
    elif "id" not in str(json_data):
        return [{"isSale": False}]
    else:
        for sale in json_data["data"]["saleEvents"]:
            if "id" not in str(sale):
                output.append({"isSale": False})
            else:
                output.append({
                    "isSale": True,
                    "tokenId": int(sale["nft"]["tokenID"]),
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
    forestSpirits(where: {
        tokenID: "%i"
    }) {
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
            "tokenId": int(json_data["data"]["forestSpirits"][0]["tokenID"]),
            "name": str(json_data["data"]["forestSpirits"][0]["name"]),
            "image_url": str(json_data["data"]["forestSpirits"][0]["image"]),
            "animation_url": str(json_data["data"]["forestSpirits"][0]["animation_url"]),
            "body": str(json_data["data"]["forestSpirits"][0]["body"]),
            "mask": str(json_data["data"]["forestSpirits"][0]["mask"]),
            "staff": str(json_data["data"]["forestSpirits"][0]["staff"]),
            "element": str(json_data["data"]["forestSpirits"][0]["element"]),
            "pedestal": str(json_data["data"]["forestSpirits"][0]["pedestal"]),
            "environment": str(json_data["data"]["forestSpirits"][0]["environment"]),
            "ancestor": str(json_data["data"]["forestSpirits"][0]["ancestor"]),
            "origin": str(json_data["data"]["forestSpirits"][0]["origin"])
        }
