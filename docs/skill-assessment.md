# 战锤 Mod 开发知识与 Skill 评估

核查日期：2026-10-14。结论：通用 Lua/规则设计、状态机、测试和工具建设可以直接开展；当前游戏的 API、CAI 行为、DB key 与存档调度必须依赖当前数据和实机结果。安装 skill 能提供流程与资料导航，不能让未知能力自动变为已验证。

本次只做发现与入口审阅，没有安装第三方 skill、注册 MCP、执行其脚本或复制第三方资料进入本仓库。

## 检索范围

检查本会话可用技能、OpenAI curated skill 目录、公开 GitHub 仓库。`skill-installer` 的目录脚本遇到网络读取不完整，随后通过 GitHub CLI 读取相同目录完成核对；该 curated 目录本次未发现战锤全战专用项。这不代表整个生态不存在。

## 候选与取舍

| 候选 | 已审阅与适用范围 | 当前判断 |
| --- | --- | --- |
| [scnjwyc/warhammer3-mod-development-skill](https://github.com/scnjwyc/warhammer3-mod-development-skill/tree/45a4c4b6dcd65557a1dbbff258f307563d60f637) | 审阅仓库说明、文件目录与 development 的完整入口；包含 DB/Lua/版本审计/本地化/UI 等导航 | 最相关的技能包候选；尚未审阅全部 references、脚本和所带资料。固定版本根目录未见明确许可证，不能将整个包当本仓库 MIT 内容复制 |
| [shen-hhao/WH3-modding](https://github.com/shen-hhao/WH3-modding/tree/83550239589742c1a261d2214ebfb29fc53daf47) | 审阅 development_generic 完整入口和根目录；仓库声明 MIT，指导 DB/Lua/RPFM 工作 | 可供比较的项目指南；入口依赖其项目上下文、目录和打包问答，需要适配，不能直接当本项目规则 |
| [PassingByPixels/wh3-mcp](https://github.com/PassingByPixels/wh3-mcp) | 仓库作者描述 Windows 游戏内执行/读取桥 | 属于调试工具而非知识 skill；仅发现线索，未代码审计/实测，当前不引入 |

第一项固定提交为 `45a4c4b6dcd65557a1dbbff258f307563d60f637`（2026-10-10），第二项为 `83550239589742c1a261d2214ebfb29fc53daf47`（2026-07-09）。公开网页或 README 可能随时变化，后续采用时重新核对。

## 对本项目的适用部分

优先考虑当前版本指纹、Lua 生命周期、DB/本地化核对、Pack 导入后读回、离线测试及证据整理。角色创建、美术和高级 UI 不是当前阶段目标；内存/反汇编流程不作为本项目的默认路线。第三方 skill 的“Agent 不启动游戏”等约定也不能未经适配覆盖本项目已授权的测试安排。

上述候选没有在入口审阅中证明可以可靠改变 CAI 长期规划或多军团集结。战略控制仍按本仓库 [API 表](research/api-register.md) 与 [MVP](mvp-boris.md) 获取证据。涉及大量附带快照与工具的技能，不应只复制单个 SKILL.md 而忽略其相对依赖。

## 建议

当前先完成 Windows E0/E1，不把 skill 安装设为前置条件。遇到具体 DB、Lua 或本地化任务时，审阅第一项对应 references 和许可后，再决定安装经核对的固定版本，或独立编写本项目的小型指南。

如果将来创建项目专用 skill，应聚焦已经在本项目验证的 Campaign AI/Chronicle 流程，使用相对路径、注明适用版本并链接 API 证据。个人目录里的全局 skill 不会随 Git clone 迁移；可复用知识与强制规则先保存在仓库内，避免另一模型/机器失去上下文。
