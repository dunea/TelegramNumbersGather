"""GetGems 采集器与响应解析工具。"""

import json
import re
from typing import Optional

import httpx


CURSOR_PATTERN = r'"cursor":\s"(.{1,32},.{1,32},.{1,32})",'
NUMBER_PATTERN = r'"(\+888\s\d{1,6}\s\d{1,6})"'


def extract_cursors(value: str) -> list[str]:
    """从 GraphQL 响应中提取分页游标。"""

    return re.findall(CURSOR_PATTERN, value)


def extract_numbers(value: str) -> list[str]:
    """从响应内容中提取 +888 手机号。"""

    return re.findall(NUMBER_PATTERN, value)


class GetgemaGather(object):
    def __init__(self, transport: Optional[httpx.AsyncBaseTransport] = None):
        self._transport = transport

    async def nft_search(self, item: str, sha256_hash: str, cursor: Optional[str] = None):
        """发起 GetGems 的 NFT 搜索请求。"""

        variables = {
            "query": json.dumps({"$and": [{"collectionAddress": item}]}),
            "attributes": None,
            "sort": json.dumps(
                [
                    {"isOnSale": {"order": "desc"}},
                    {"price": {"order": "asc"}},
                    {"index": {"order": "asc"}},
                ]
            ),
            "count": 28,
        }
        if cursor:
            variables["cursor"] = cursor

        extensions = {"persistedQuery": {"version": 1, "sha256Hash": sha256_hash}}

        async with httpx.AsyncClient(transport=self._transport) as client:
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
