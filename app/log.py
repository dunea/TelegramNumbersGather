"""项目统一日志配置与获取入口。"""

from __future__ import annotations

import logging
from typing import Final


_DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_DEFAULT_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
_HANDLER_FLAG: Final[str] = "_telegram_numbers_gather_handler"


def setup_logging(level: int = logging.INFO) -> None:
    """初始化项目日志配置，保证控制台输出格式一致且可重复调用。"""

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if getattr(handler, _HANDLER_FLAG, False):
            root_logger.setLevel(level)
            logging.getLogger("httpx").setLevel(logging.WARNING)
            logging.getLogger("httpcore").setLevel(logging.WARNING)
            return

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(_DEFAULT_LOG_FORMAT, _DEFAULT_DATE_FORMAT))
    setattr(handler, _HANDLER_FLAG, True)

    root_logger.setLevel(level)
    root_logger.addHandler(handler)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str | None = None) -> logging.Logger:
    """获取项目 logger，首次调用时自动完成基础初始化。"""

    setup_logging()
    return logging.getLogger(name)
