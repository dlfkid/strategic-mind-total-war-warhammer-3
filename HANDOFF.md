# 跨模型与跨机器交接

Updated: 2026-10-14

先读 [RULES.md](RULES.md)。本文件描述最新可接续状态；详细证据在相关文档，提交号以 Git 实际记录为准，不能只凭聊天恢复项目。

## 当前状态

阶段：仓库准备已完成本轮建设，下一阶段到 Windows 游戏环境验证。已完成首轮可行性调查和文档初始化，前置基线为 `fdc8177`。当前工作在 Mac 的原仓库直接进行。

没有 Mod 功能、发行 `.pack` 或游戏测试。17 项 [API](docs/research/api-register.md) 全部 `NOT_RUN`。公开补丁参考是调查日的 9.0.3，实际测试机版本/Build ID 尚未采集。

当前 Git 远端为 `dlfkid/strategic-mind-total-war-warhammer-3`。初始化与本轮建设尚待同步远端；本地完成不表示 Windows clone 已能获取。接续时检查 `git status -sb` 和 `git log --oneline origin/main..HEAD`，不要假定本文描述的同步状态永远不变。

## 本轮变更

- 建立 `RULES.md` 单一规则来源，`AGENTS.md`、`CLAUDE.md`、Copilot 与 Cursor 入口统一引导到规则和交接。
- 增加跨平台仓库检查、提交 hook 和 GitHub Actions；检查暂存区的交接更新，以及提交范围内每个新提交，防止后补交接掩盖先前遗漏。
- 增加 Mac/Windows 开发工作流、迁移清单、skill 评估与统一换行规则。没有安装第三方 skill、MCP 或游戏工具。
- 当前 clone 已启用仓库本地 pre-commit hook（`.git/config` 的 `core.hooksPath=.githooks`）；hook 配置不会随 clone 自动继承，下一端必须重新启用。

## 已执行的验证

本机 Python 3.14.3、Git 可用。`python3 -m unittest discover -s tests -v` 的 21 项测试全部通过，覆盖遗漏交接、未暂存交接、空白/日期改动、暂存区/工作目录差异、逐提交检查、删除规则绕过尝试、新分支历史检查，以及受限编码下的中文诊断。

仓库文档/链接检查、`--staged` 和 `git diff --cached --check` 均通过；具体命令见 [开发工作流](docs/development-workflow.md)。已直接验证本地 hook：未暂存交接时拒绝，补齐后通过；hook 已保存为可执行文件。GitHub Actions 已配置 Linux/Windows，但尚未推送触发，不能称远端或 Windows 已通过。

## 未验证与阻塞

- 本机未找到游戏常见安装路径、RPFM 命令或 Assembly Kit；详见 [环境记录](docs/research/environment.md)。尚不能完成 E0 或任何实机 API 结论。
- Windows 上的 Git、Python、hook、RPFM、游戏版本、日志目录与测试档均待实际核对。仓库检查通过不代表游戏工具链通过。
- [Skill 评估](docs/skill-assessment.md) 已发现相关候选并审阅入口，未审计整个包、未安装。适合之后按实际任务选择；不是开始验证的前提。
- 尚未设置分支保护；本地 hook 可被人为绕过，CI 尚未触发。规则与检查不能保证任意未加载规则的模型自觉遵守。

## 下一步

1. 取得推送授权后将本地初始化和本轮建设同步远端，再由 Windows clone 接续；若暂不推送，可用 Git bundle 传递已提交历史。本轮提交位置用 `git log -1` 核对。
2. 按 [Windows 接续清单](docs/windows-development.md) 安装/核对基础工具，启用 hook，运行仓库检查和测试。
3. 在实际 Windows 游戏机收集平台、补丁号/Build ID、DLC、Mod 列表与顺序、语言、难度和可重复加载的存档。原始文件只放 `local/`、`artifacts/`。
4. 核对当前原版脚本入口、鲍里斯身份、相关 DB/消息 key，随后只实现 [MVP E0](docs/mvp-boris.md) 的最小加载和日志探针。成功后更新 API-01、API-07 与本文件，再做 E1。

不要直接开发完整战略引擎、复制旧版本 key，或把原版鲍里斯已有的野兽人通知当作本项目效果。

## 跨 clone 接续

仓库无需旧 clone 的绝对路径、聊天记录或个人 skill 目录。新模型先读 RULES → HANDOFF → README → 对应实验文档。只克隆 Git 会取得源码/文档/检查器，不会取得本地 hook 配置、游戏数据、私有日志或系统级 skill。

Mac 的 `python3` 命令在 Windows 通常换成 `py -3`；路径从 clone 根目录解析。每个 clone 检查是否已有 `core.hooksPath`，无冲突后设为 `.githooks`。GitHub 同步与本地环境接入分别记录；迁移完成时用本文件的新证据替换未完成状态，不复制 Mac 的安装结论。

## 最近里程碑

- 2026-10-14：`fdc8177` 完成可行性文档与 17 项待测 API 清单。
- 2026-10-14：建立跨模型规则、交接、提交检查、CI 与 Windows 接续流程；本轮提交号以 `git log -1` 为准。
