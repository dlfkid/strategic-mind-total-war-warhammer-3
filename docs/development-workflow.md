# 开发与交接工作流

所有参与者先阅读 [RULES](../RULES.md) 和 [HANDOFF](../HANDOFF.md)。流程不依赖某台机器的路径或某个模型的记忆。

## 新 clone 的一次性设置

需要 Git 与 Python 3.10+，不需要第三方 Python 包。先检查已有 hook 配置：

```text
git config --show-origin --get core.hooksPath
```

没有输出通常表示未设置（该命令可能返回 1）；若已有其他路径，先查看并协调现有 hooks，不覆盖。没有冲突时在当前仓库启用：

```text
git config --local core.hooksPath .githooks
```

Git 不会自动在新 clone 中启用仓库 hook，必须每台机器/每个 clone 设置。`pre-commit` 使用 Git 自带 shell，在 Windows 优先找 `py -3`，然后是 `python3` 或 `python`。文件必须保持 LF 和可执行位；仓库已用 `.gitattributes` 管理换行。

## 一轮建设

1. 检查分支、工作区与远端状态，读交接及相关文档。确认本机环境而非沿用旧机路径。
2. 做本次任务内的变更，按需更新 API、来源和测试记录。
3. 更新 `HANDOFF.md`：本轮变化、验证证据、未完成项和下一步。纯问答不制造无意义更新。
4. 运行检查/测试，明确暂存本轮文件与交接，再检查暂存快照，最后提交。

Mac/Linux 的检查命令：

```sh
python3 tools/check_repository.py
python3 -m unittest discover -s tests -v
python3 tools/check_repository.py --staged
git diff --cached --check
```

Windows PowerShell：

```powershell
py -3 tools/check_repository.py
py -3 -m unittest discover -s tests -v
py -3 tools/check_repository.py --staged
git diff --cached --check
```

检查器/提交规则变更应跑完整测试；纯文档变更通常只需文档和暂存区检查。默认检查工作目录，`--staged` 专门检查即将提交的 Git index，包括链接指向的文件是否也在暂存快照里。只在工作目录改交接而未暂存会失败。

## 提交检查与 CI

本地 hook 对任何非 `HANDOFF.md` 的暂存文件变更，要求同一提交包含实质性交接更新。文档、配置、删除/重命名也在范围内。比较时忽略空白与 `Updated` 行，因此只加空行或改日期不能通过；其他敷衍文字仍需人工/模型审查。

CI 运行检查器测试和文档检查，并对基准之后的每个提交检查交接，不允许通过“下一次提交补交接”掩盖遗漏。规则引入之前的历史提交不追溯要求交接。新分支首次推送或手动触发没有有效 before SHA 时，检查全部可取得的历史。缺少基准对象时失败并要求获取完整历史，不能静默跳过。

本地也能检查一段已经提交的历史：

```text
python3 tools/check_repository.py --base origin/main
```

Windows 将 `python3` 换为 `py -3`。CI 分别配置 Linux 与 Windows，使用 Python 标准库；它验证仓库流程，不启动游戏、不制作包、不验证 Mod 行为。

本地 hook 可被人为跳过，CI 也只能在推送之后给出结果。若要禁止失败变更进入主分支，需要由管理员把相应 CI 检查设为分支保护的必需检查；本次未修改远端权限或保护设置。

## 故障与交接内容

暂存区检查失败时先看报告，补齐准确交接或修复缺失文件，再暂存并复查。不要关闭 hook 或制造虚假的测试结果。已分享的违规提交不自行重写历史；如需例外修复，由维护者决定并明确记录。

交接不嵌入它自身尚未生成的提交哈希，避免“为更新哈希又提交一次”的循环。详细日志和临时数据放在忽略目录，交接只保留路径说明、必要哈希与结论。准备换机器时，确保下一端能够取得对应 Git 提交，并记录哪些本地文件还需要另行复制。
