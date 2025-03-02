import json

import httpx


class GetgemaGather(object):
    def __init__(self):
        pass
    
    async def nft_search(self, item: str, sha256_hash: str, cursor: str = None):
        variables = {
            "query": json.dumps({"$and": [{"collectionAddress": item}]}),
            "attributes": None,
            "sort": json.dumps(
                [{"isOnSale": {"order": "desc"}}, {"price": {"order": "asc"}}, {"index": {"order": "asc"}}]),
            "count": 28,
        }
        if cursor:
            variables["cursor"] = cursor
        
        extensions = {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": sha256_hash
            }
        }
        
        async with httpx.AsyncClient() as client:
            result = await client.get(
                "https://getgems.io/graphql/",
                headers={
                    "accept": "*/*",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "content-type": "application/json",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                },
                params={
                    "operationName": "nftSearch",
                    "variables": json.dumps(variables),
                    "extensions": json.dumps(extensions),
                },
            )
            result.raise_for_status()
        
        return result.json()
