# Strategic Mind — Every Lord Has a Purpose

面向《Total War: Warhammer III》Immortal Empires（超凡帝国）的长期 Mod 项目。

每一位传奇领主都应该拥有符合其背景、文化和性格的战略目的。项目关注战争的意义、决策的连续性，以及世界如何记住并回应玩家的行为。

> Decisions create consequences. Consequences create history. History becomes narrative when observed.

## 当前状态

2026-10-14：完成第一轮公开资料调查，建立跨模型规则、交接文档、提交检查与 Windows 接续流程。**没有可安装的 Mod，没有生成 `.pack`，没有进行游戏内 API 测试。**

官方当前公开版本参考为 [9.0.3（2026-10-09）](https://community.creative-assembly.com/total-war/total-war-warhammer/forums/7-patch-notes-amp-announcements/threads/16126-total-war-warhammer-iii-patch-9-0-3)。本机未发现游戏与开发工具的常见安装位置，实际安装版本和 Steam Build ID 尚未取得；这不是 9.0.3 兼容性声明。

初步判断：World Memory 与原版消息形式的 Strategic Chronicle 有文档级依据；战略态度、性格和有限行动干预有候选接口；多军团集结、长期自主计划和通用 Battle AI 控制仍需验证。

## 三个 Mod

| 组件 | 优先级 | 职责与边界 |
| --- | --- | --- |
| Campaign AI | P0 | 三层决策、世界记忆、有限战略干预、战略纪事；先验证一个地区与一个领主 |
| Victory Conditions | P1 | 派系使命及胜利目标；独立安装，正式胜利与 Steam 成就分别验证 |
| Battle AI | P2 | 独立调查战斗脚本加载、单位控制与归还；具体战术实验以接口验证结果为前提 |

三个 Mod 的运行时依赖默认独立。Chronicle 与 Memory 首先是 Campaign AI 的内部能力，不额外发行第四个基础依赖包。

## 文档入口

- [HANDOFF.md](HANDOFF.md)：任何 clone 或新模型接续时先读的最新状态。
- [RULES.md](RULES.md)：统一项目规则，要求每次建设更新交接并与变更一起提交。
- [开发与交接工作流](docs/development-workflow.md)：本地 hook、跨平台检查与 CI。
- [Windows 接续清单](docs/windows-development.md)：同步仓库、准备环境与第一个实机实验。
- [Skill 评估](docs/skill-assessment.md)：知识边界、已找到的专用指南与当前采用建议。
- [项目目标与设计原则](docs/design-principles.md)：范围、三层模型、真实因果、战争迷雾和模块边界。
- [技术可行性报告](docs/research/feasibility.md)：当前结论、工具链、战略控制、纪事、胜利与战斗能力。
- [调查来源](docs/research/sources.md)：官方公告、CA 脚本文档镜像、固定版本的 RPFM schema。
- [本地环境记录](docs/research/environment.md)：已经检查的条件与缺失项。
- [API 验证记录](docs/research/api-register.md)：候选接口、证据等级、实机实验及尚未验证的结果。
- [鲍里斯—野兽人 MVP](docs/mvp-boris.md)：实验顺序、观测标准、替代实验与止损条件。
- [兼容性与测试规划](docs/testing-and-compatibility.md)：存档、性能、共存、更新回归和证据要求。
- [路线图](docs/roadmap.md)：下一阶段行动及进入后续阶段的条件。
- [AGENTS.md](AGENTS.md)：在本仓库工作的开发约定。

## 仓库结构

当前包含项目文档、模型规则入口、`tools/` 仓库检查器、`tests/` 检查器测试，以及本地 hook/CI。测试只验证仓库流程，不模拟游戏能力。取得实机条件后再增加 `mods/campaign-ai/`、`mods/victory-conditions/`、`mods/battle-ai/`，不提前建立空框架或选择游戏打包流水线。

新 clone 需要 Git、Python 3.10+，并按 [开发工作流](docs/development-workflow.md) 单独启用 `.githooks`。规则文档随 Git 传递，本地 hook 配置和系统级 skill 不会自动传递。

未来 Campaign AI 的纯决策逻辑与游戏适配逻辑必须分离；具体加载路径、依赖和 `.pack` 内容由最小加载实验决定。仓库保存原创源码、少量测试样例和验证结论，游戏原始文件、个人存档与临时日志保存在本地忽略目录。

## 下一步

取得一个可运行游戏的测试环境，记录平台、游戏版本、Build ID、DLC、Mod 列表和加载顺序；从当前安装导出相关脚本及 DB 记录，然后执行 [MVP 的环境与观察实验](docs/mvp-boris.md)。优先回答“有无可靠的干预与反馈闭环”，再扩大决策模型。

## 许可

本仓库原创内容沿用现有 [MIT License](LICENSE)。游戏、Warhammer 设定及第三方工具的权利归各自权利人；MIT 不授予第三方素材的再分发权。
