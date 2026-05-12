import json
import unittest

import httpx

from app.getgema_gather import GetgemaGather, extract_cursors, extract_numbers


class ParseHelpersTest(unittest.TestCase):
    def test_extract_cursors(self) -> None:
        value = '{"cursor": "T,123,12345678", "other": 1}'
        self.assertEqual(extract_cursors(value), ["T,123,12345678"])

    def test_extract_numbers(self) -> None:
        value = '{"phone": "+888 123 456"}'
        self.assertEqual(extract_numbers(value), ["+888 123 456"])


class GetgemaGatherTest(unittest.IsolatedAsyncioTestCase):
    async def test_nft_search_without_cursor(self) -> None:
        seen: dict[str, str] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            seen["operationName"] = request.url.params["operationName"]
            seen["variables"] = request.url.params["variables"]
            seen["extensions"] = request.url.params["extensions"]
            return httpx.Response(200, json={"ok": True})

        gather = GetgemaGather(transport=httpx.MockTransport(handler))
        result = await gather.nft_search("item", "sha256", None)

        self.assertEqual(result, {"ok": True})
        self.assertEqual(seen["operationName"], "nftSearch")

        variables = json.loads(seen["variables"])
        self.assertEqual(variables["count"], 28)
        self.assertNotIn("cursor", variables)

        extensions = json.loads(seen["extensions"])
        self.assertEqual(extensions["persistedQuery"]["version"], 1)
        self.assertEqual(extensions["persistedQuery"]["sha256Hash"], "sha256")

    async def test_nft_search_with_cursor(self) -> None:
        seen: dict[str, str] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            seen["variables"] = request.url.params["variables"]
            return httpx.Response(200, json={"ok": True})

        gather = GetgemaGather(transport=httpx.MockTransport(handler))
        await gather.nft_search("item", "sha256", "T,123,12345678")

        variables = json.loads(seen["variables"])
        self.assertEqual(variables["cursor"], "T,123,12345678")


if __name__ == "__main__":
    unittest.main()
