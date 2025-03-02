import httpx


class TonviewerGather:
    def __init__(self):
        pass
    
    async def collections(self, item: str, limit=0, offset=50):
        gather_url = f"https://tonapi.io/v2/nfts/collections/{item}/items?limit={limit}&offset={offset}"
        async with httpx.AsyncClient() as client:
            result = await client.get(gather_url)
            result.raise_for_status()
        
        pass
