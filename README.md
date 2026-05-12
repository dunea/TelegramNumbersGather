# Telegram Numbers Gather

这是一个基于 Python + SQLAlchemy 的号码采集脚本项目，默认从 GetGems 拉取数据并写入本地 SQLite 数据库 `data.db`。

## 运行方式

直接执行入口文件即可启动采集：

```bash
python -m cmd.run
```

也可以自定义参数：

```bash
python -m cmd.run --max-pages 100 --retry-times 3 --sleep-seconds 1
```

## 测试

测试目录里的脚本已经整理成真正的单元测试，重点覆盖响应解析和 `nft_search` 的请求参数构造：

```bash
python -m unittest
```

## 说明

- `cmd/run.py` 是主入口，只负责启动、分页采集和落库。
- `app/getgema_gather.py` 负责请求 GetGems 接口并提供响应解析工具。
- `test/` 目录现在用于单元测试，不再放采集主流程脚本。
