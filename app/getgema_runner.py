"""GetGems 采集编排逻辑。"""

from __future__ import annotations

import argparse
import asyncio
import json
from collections.abc import Sequence
from dataclasses import dataclass

from app.database import Base, Session, engine
from app import models
from app.getgema_gather import GetgemaGather, extract_cursors, extract_numbers

DEFAULT_ITEM = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"
DEFAULT_SHA256_HASH = "af904314608b2384958183c1c667de0028660f25c628a6a0ae9512e8c70a840e"
DEFAULT_MAX_PAGES = 4878
DEFAULT_RETRY_TIMES = 3
DEFAULT_SLEEP_SECONDS = 1.0


@dataclass(slots=True)
class GetgemaRunConfig:
    """GetGems 采集运行参数。"""

    item: str = DEFAULT_ITEM
    sha256_hash: str = DEFAULT_SHA256_HASH
    max_pages: int = DEFAULT_MAX_PAGES
    retry_times: int = DEFAULT_RETRY_TIMES
    sleep_seconds: float = DEFAULT_SLEEP_SECONDS


def build_parser() -> argparse.ArgumentParser:
    """构造命令行参数解析器。"""

    parser = argparse.ArgumentParser(description="启动 GetGems 号码采集并写入本地数据库")
    parser.add_argument("--item", default=DEFAULT_ITEM, help="GetGems collectionAddress")
    parser.add_argument("--sha256-hash", default=DEFAULT_SHA256_HASH, help="GraphQL persistedQuery 的 sha256Hash")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="最大采集页数")
    parser.add_argument("--retry-times", type=int, default=DEFAULT_RETRY_TIMES, help="单页失败重试次数")
    parser.add_argument("--sleep-seconds", type=float, default=DEFAULT_SLEEP_SECONDS, help="每次请求前的等待秒数")
    return parser


def parse_args(argv: Sequence[str] | None = None) -> GetgemaRunConfig:
    """解析命令行参数并转换为运行配置。"""

    args = build_parser().parse_args(argv)
    return GetgemaRunConfig(
        item=args.item,
        sha256_hash=args.sha256_hash,
        max_pages=args.max_pages,
        retry_times=args.retry_times,
        sleep_seconds=args.sleep_seconds,
    )


def ensure_database() -> None:
    """确保本地 SQLite 表结构已创建。"""

    Base.metadata.create_all(bind=engine)


def save_numbers(numbers: Sequence[str]) -> int:
    """批量写入未存在的号码，返回新增条数。"""

    unique_numbers = list(dict.fromkeys(numbers))
    if not unique_numbers:
        return 0

    with Session() as session:
        existing_numbers = {
            row[0]
            for row in session.query(models.ThreeEightsNumbers.number)
            .filter(models.ThreeEightsNumbers.number.in_(unique_numbers))
            .all()
        }
        pending_numbers = [number for number in unique_numbers if number not in existing_numbers]
        if not pending_numbers:
            return 0

        # 统一批量写入，减少逐条提交带来的性能损耗。
        session.add_all(models.ThreeEightsNumbers(number=number) for number in pending_numbers)
        session.commit()
        return len(pending_numbers)


async def crawl_getgema_numbers(config: GetgemaRunConfig) -> int:
    """按分页循环抓取号码并保存，返回新增号码总数。"""

    gather = GetgemaGather()
    cursor: str | None = None
    inserted_total = 0

    for page_index in range(config.max_pages):
        for retry_index in range(config.retry_times):
            try:
                if config.sleep_seconds > 0:
                    await asyncio.sleep(config.sleep_seconds)

                # 先拉取当前页，再从响应中提取游标和号码。
                result = await gather.nft_search(config.item, config.sha256_hash, cursor)
                json_str = json.dumps(result)

                cursors = extract_cursors(json_str)
                if not cursors:
                    print(f"第 {page_index + 1} 页 - 没有更多游标，采集结束")
                    return inserted_total

                cursor = cursors[-1]
                print(f"next cursor - {cursor}")

                numbers = [number.replace(" ", "") for number in extract_numbers(json_str)]
                print(f"第 {page_index + 1} 页 - {numbers}")

                inserted_count = save_numbers(numbers)
                inserted_total += inserted_count
                print(f"第 {page_index + 1} 页 - 新增 {inserted_count} 条，累计 {inserted_total} 条")
                break
            except Exception as exc:
                print(f"第 {page_index + 1} 页 - 第 {retry_index + 1} 次采集失败 - {exc}")
                if retry_index + 1 == config.retry_times:
                    print(f"第 {page_index + 1} 页 - 达到最大重试次数，继续下一页")

    return inserted_total


async def run(argv: Sequence[str] | None = None) -> int:
    """解析参数、初始化数据库并执行采集。"""

    config = parse_args(argv)
    ensure_database()
    return await crawl_getgema_numbers(config)