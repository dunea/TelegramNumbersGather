"""命令行入口。"""

import asyncio

from app.log import get_logger
from app.getgema_runner import run


logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("程序启动")
    asyncio.run(run())
    logger.info("程序结束")
