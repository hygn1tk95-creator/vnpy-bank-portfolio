# 基于 vn.py 的量化研究与模拟交易平台

> An event-driven quantitative research and paper-trading platform built on vn.py.

## 项目简介

本项目基于 vn.py 4.4.0 进行二次开发，目标是构建一套可在 Linux 服务器运行的量化研究、回测、模拟交易与运行监控平台。

项目当前聚焦工程闭环：事件驱动架构、策略开发、历史数据存储、成本敏感回测、风险控制和后续 Web 管理能力。

> 当前 DEMO 数据为可复现的合成 K 线，仅用于验证数据入库与回测链路，不构成投资建议或真实策略绩效。

## 已完成能力

- [x] Ubuntu 22.04 + Conda Python 3.13 隔离运行环境
- [x] vn.py 4.4.0 源码可编辑安装
- [x] 事件引擎与主引擎健康检查
- [x] SQLite 历史数据存储与查询
- [x] 可复现 DEMO K 线数据生成与入库
- [x] 双均线 CTA 策略开发
- [x] 包含手续费、滑点、合约乘数和最小价位的无 GUI 回测
- [ ] 真实历史数据接入
- [ ] 模拟账户或 SimNow 仿真交易
- [ ] 事前风控配置
- [ ] systemd 后台守护与日志告警
- [ ] Web 管理台与演示部署

## 架构概览

```text
历史数据 / 行情接口
        │
        ▼
vn.py Gateway / Datafeed
        │
        ▼
EventEngine ───────────────► Log / Monitoring
        │
        ▼
MainEngine + OMS
        │
        ├── CTA Strategy
        ├── Backtesting Engine
        ├── Risk Manager
        └── Paper Account / SimNow
        │
        ▼
SQLite / PostgreSQL
        │
        ▼
Web Management Dashboard

## 技术栈
- Python 3.13
- vn.py 4.4.0
- Conda、pip、Git
- SQLite
- Pandas、NumPy、TA-Lib
- Linux / Ubuntu
- 后续：FastAPI、systemd、Nginx 或 Caddy、Docker

## 项目结构
vnpy-bank-portfolio/
├── strategies/                 # 自定义 CTA 策略
├── scripts/                    # 验证、数据入库和回测脚本
├── docs/                       # 架构、部署、演示文档
├── config/                     # 不含密钥的配置模板
├── deploy/                     # 服务部署文件
├── tests/                      # 自动化测试
└── .vntrader/                  # 本地数据库、日志和运行配置（不提交）

快速验证
在已创建的 vnpy313 Conda 环境中运行：
cd /home/b115/huiming/vnpy-bank-portfolio

python scripts/smoke_test.py
python scripts/event_demo.py
python scripts/verify_database.py
python scripts/seed_demo_bars.py
python scripts/run_demo_backtest.py
回测说明
当前回测标的为 DEMO.CFFEX，使用固定公式生成的 480 根一分钟 K 线，以保证每次执行结果可复现。
回测中显式设置：
- 初始资金；
- 手续费率；
- 滑点；
- 合约乘数；
- 最小报价单位。
因此，回测结果用于验证策略和成本计算流程，而非评价真实投资收益。
安全与风险边界
- .vntrader/、数据库、日志、账户配置和密钥均通过 .gitignore 排除；
- 公共 Web 演示仅展示脱敏 DEMO 数据、策略状态、回测指标和风控事件；
- 不将真实券商凭据、交易接口密钥或下单能力暴露到公网；
- 真实交易接入前必须完成历史验证、仿真验证、风控配置和权限隔离。
后续规划
1. 接入真实历史数据并进行样本内、样本外回测；
2. 配置 PaperAccount 或 CTP SimNow 仿真；
3. 启用 RiskManager，限制单笔数量、订单频率和撤单次数；
4. 使用 systemd 管理策略服务，增加自动重启和日志告警；
5. 开发只读优先的 FastAPI Web 管理台；
6. 部署公开 DEMO 页面并录制项目演示视频。

保存后执行：

```bash
cd /home/b115/huiming/vnpy-bank-portfolio
git add README.md
git diff --cached --check
git diff --cached --stat
git status --short