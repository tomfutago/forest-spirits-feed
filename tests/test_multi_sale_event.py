from forest_spirits_feed.graphql import *

def getSaleEventPerBlockTest(block: int) -> list[dict]:
    query = """query {
    saleEvents(
      orderBy: idx
      orderDirection: asc
      where: {
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
    #print(len(json_data["data"]["saleEvents"]))

    #for sale in json_data["data"]["saleEvents"]:
    #    print(sale)
    
    output = []
    if "error" in str(json_data):
        return {"isSale": False}
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

saleEvent = getSaleEventPerBlockTest(14464050)
#print(saleEvent)
for n in range(len(saleEvent)):
    print(n, saleEvent[n]["tokenId"])

print([{"isSale": False}])
