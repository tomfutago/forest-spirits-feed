import json
import pandas as pd
import requests

i = 1
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

url = "https://api.thegraph.com/subgraphs/name/tomfutago/forest-spirits"
r = requests.post(url, json={"query": query})
#print(r.status_code)
json_data = json.loads(r.text)
#print(json.dumps(json_data, indent=2))
#df_tmp = pd.json_normalize(json_data["data"]["saleEvents"])
#if i == 1: # only once
#    df = pd.concat([df_tmp])
#else:
#    df = pd.concat([df, df_tmp])
#print(df_tmp)

idx = int(json_data["data"]["saleEvents"][0]["nft"]["id"])
print(idx)

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
  """ % (idx)


url = "https://api.thegraph.com/subgraphs/name/tomfutago/forest-spirits"
r = requests.post(url, json={"query": query})
#print(r.status_code)
json_data = json.loads(r.text)
print(json.dumps(json_data, indent=2))

name = json_data["data"]["forestSpirit"]["name"]
print(name)
