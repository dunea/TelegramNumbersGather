# Telegram +888 号码采集工具 | Python SQLAlchemy 数据库项目

一个高效的 **Telegram 号码采集爬虫项目**，使用 Python + SQLAlchemy + Alembic 从 GetGems API 采集 Telegram 用户号码，已采集 **13.6 万条** +888 号码数据。支持分页采集、参数定制、数据库持久化和单元测试。

> 📦 **预置数据文件**：`three_eights_numbers.json` 包含全部采集数据（13.6w条），开箱即用，无需重新采集。
> 🔗 **直链下载**：<https://raw.githubusercontent.com/dunea/TelegramNumbersGather/refs/heads/master/three_eights_numbers.json>

---

## 📋 目录

- [项目特点](#项目特点)
- [系统要求](#系统要求)
- [安装指南](#安装指南)
- [快速开始](#快速开始)
- [命令参数](#命令参数)
- [项目结构](#项目结构)
- [测试方法](#测试方法)
- [数据库迁移](#数据库迁移)
- [常见问题](#常见问题)
- [许可证](#许可证)

---

## ✨ 项目特点

- ✅ **完整的号码采集流程**：支持从 GetGems NFT 平台采集 Telegram 用户号码
- ✅ **SQLite 数据库存储**：使用 SQLAlchemy ORM 管理号码数据，支持 Alembic 数据库迁移
- ✅ **灵活的参数配置**：支持自定义分页数量、重试次数、请求间隔
- ✅ **单元测试覆盖**：完整的单元测试框架，覆盖 API 响应解析和参数构造
- ✅ **生产级数据集**：预置 13.6 万条真实 Telegram +888 号码，JSON 格式导出
- ✅ **错误处理与日志**：结构化日志输出，详细的异常捕获和重试机制

---

## 🔧 系统要求

- **Python 版本**：3.8 及以上
- **操作系统**：Windows / macOS / Linux
- **网络**：需要能访问 GetGems API 接口
- **存储**：至少 50MB 空间用于 SQLite 数据库

---

## 📥 安装指南

### 1. 克隆或下载项目

```bash
git clone https://github.com/dunea/TelegramNumbersGather.git
cd TelegramNumbersGather
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 基础运行

直接执行入口文件启动号码采集：

```bash
python -m cmd.run
```

### 自定义参数运行

```bash
# 采集前 100 页，重试 3 次，每次请求间隔 1 秒
python -m cmd.run --max-pages 100 --retry-times 3 --sleep-seconds 1
```

---

## 📊 命令参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--max-pages` | int | 所有页 | 最大采集分页数 |
| `--retry-times` | int | 3 | 单个请求最大重试次数 |
| `--sleep-seconds` | float | 0.5 | 请求间隔（秒） |

---

## 📁 项目结构

```
TelegramNumbersGather/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python 依赖列表
├── alembic.ini                  # Alembic 数据库迁移配置
├── three_eights_numbers.json    # 预置采集数据（13.6w 条号码）
├── alembic/                     # 数据库迁移脚本目录
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                # 迁移版本历史
├── app/                         # 业务逻辑层
│   ├── __init__.py
│   ├── database.py              # 数据库连接配置
│   ├── models.py                # SQLAlchemy 数据模型
│   ├── getgema_gather.py        # GetGems API 采集工具
│   ├── tonviewer_gather.py      # TonViewer API 采集工具（备用）
│   ├── getgema_runner.py        # 采集运行器
│   └── log.py                   # 日志配置
├── cmd/                         # 命令行入口
│   ├── __init__.py
│   └── run.py                   # 主入口脚本
└── test/                        # 单元测试
    ├── __init__.py
    └── test_getgema_gather.py   # GetGems 采集测试
```

### 核心模块说明

| 模块 | 文件 | 职责 |
|-----|------|------|
| **数据采集** | `app/getgema_gather.py` | 请求 GetGems NFT API，解析响应数据，提取号码 |
| **数据持久化** | `app/database.py` | SQLite 连接配置，数据库初始化 |
| **数据模型** | `app/models.py` | SQLAlchemy ORM 模型定义 |
| **运行器** | `app/getgema_runner.py` | 分页采集逻辑，异常处理，重试机制 |
| **命令行** | `cmd/run.py` | 参数解析，采集流程编排 |

---

## 🧪 测试方法

运行完整的单元测试套件：

```bash
python -m unittest discover -s test -p "test_*.py" -v
```

运行特定测试文件：

```bash
python -m unittest test.test_getgema_gather -v
```

### 测试覆盖范围

- ✅ GetGems API 响应解析
- ✅ `nft_search` 请求参数构造
- ✅ 号码提取和数据验证
- ✅ 异常处理和重试逻辑

---

## 🔄 数据库迁移

项目集成 Alembic 用于数据库版本管理。

### 生成新的迁移

```bash
alembic revision --autogenerate -m "描述变更内容"
```

### 应用迁移

```bash
alembic upgrade head
```

### 查看迁移历史

```bash
alembic history
```

---

## ❓ 常见问题

### Q: 我应该使用预置的 JSON 数据还是自己采集？

**A:** 推荐直接使用 `three_eights_numbers.json`（已包含 13.6 万条号码，采集完成）。如需更新数据，可运行采集脚本。

### Q: 采集速度太慢怎么办？

**A:** 可调整参数降低 `--sleep-seconds`（减少请求间隔），但需注意 API 速率限制。

### Q: 如何导出数据为 CSV 或其他格式？

**A:** 数据存储在 SQLite `data.db` 中，可使用 SQLite 工具或 Python 脚本导出。

### Q: GetGems API 返回 403 或限流怎么办？

**A:** 增大 `--sleep-seconds` 或 `--retry-times`，或在不同时间段重试。

---

## 📝 依赖说明

| 包名 | 用途 |
|-----|------|
| `sqlalchemy` | ORM 数据库框架 |
| `alembic` | 数据库迁移工具 |
| `requests` | HTTP 请求库 |

详见 [requirements.txt](requirements.txt)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 改进此项目。

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

- [GetGems 官网](https://getgems.io/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Alembic 文档](https://alembic.sqlalchemy.org/)
- [Python 官方文档](https://docs.python.org/)

---

**最后更新**：2026 年 5 月 13 日 | **维护者**：[@dunea](https://github.com/dunea)
