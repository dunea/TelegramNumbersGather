"""命令行入口。"""

import asyncio
import sys
from pathlib import Path

# 兼容 `python cmd/run.py` 直接运行：将项目根目录加入模块搜索路径。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.log import get_logger
from app.getgema_runner import run

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("程序启动")
    asyncio.run(run())
    logger.info("程序结束")
