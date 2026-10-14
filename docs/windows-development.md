# Windows 接续清单

当前策略：先在 Mac 完成仓库准备；早期 API 探路在有游戏的 Windows 机上完成编辑、打包、运行和日志查看的循环。以后可用 Mac 编写纯逻辑，通过 Git 同步到 Windows。

## 取得相同代码

确认 Mac 上的提交已保存，并在取得对应授权后推送远端。当前仓库未自动推送，因此仅在 Windows 克隆远端可能仍只能看到许可证。以实际远端日志核对，不凭本文推断已同步。

远端同步后，在 Windows PowerShell：

```powershell
git clone https://github.com/dlfkid/strategic-mind-total-war-warhammer-3.git
cd strategic-mind-total-war-warhammer-3
git status -sb
git log -3 --oneline
```

如果 Windows 已有 clone，先保护它的未提交工作，再获取远端并同步对应分支；`git pull --ff-only` 不会自动覆盖本地分叉，失败时先检查，不做强制重置。

若不使用远端，可在源 clone 创建包含已提交历史的 Git bundle，传到 Windows 后克隆。不要用复制 `.git` 或叠加覆盖目录代替同步，也不要把运行中的游戏目录当作源码仓库。

## 基础工具与仓库检查

- 安装/核对 Git for Windows 与 Python 3.10+；`git --version`、`py -3 --version` 应可运行。
- 阅读根目录的 RULES、HANDOFF、README。按 [开发工作流](development-workflow.md) 检查既有 hook 配置，再启用 `.githooks`。
- 运行 `py -3 tools/check_repository.py` 和 `py -3 -m unittest discover -s tests -v`。通过后仅表示仓库工具工作正常。
- 本地系统配置与游戏导出放 `local/`，测试结果放 `artifacts/`；它们不随 clone 自动同步。

## 游戏与 Mod 工具

使用实际安装的游戏、[RPFM 官方发布](https://github.com/Frodo45127/rpfm/releases) 与对应 WH3 schema；Assembly Kit 按读取定义和具体实验的需要准备。先记录版本并确认能读取包，不为最小 Lua 实验预装全部地图/美术工具。

记录以下事实到环境/API 记录，再更新 HANDOFF：游戏平台、游戏主菜单版本、Build ID、DLC、活动 Mod 与加载顺序、语言、难度、测试档回合、RPFM/schema 版本。游戏路径可能位于其他盘，以 Steam 实际安装位置为准。

当前 Mac 的“未发现安装”仅是那台机器的调查结果；Windows 接续要追加自己的记录，不能删除旧记录并假装此前已测。Steam manifest 中的 Build ID 与公开补丁号分开保存。

## 第一个游戏实验

先核对当前原版加载入口、日志机制和所需 key，随后只开发 [E0](mvp-boris.md) 的加载标记/日志探针。取得当前版本下的新局与旧档证据，更新 API-01、API-07 与 HANDOFF，再进入事件/记忆实验。

这一阶段需要正常启动/重载游戏。日后如引入自动执行桥，先单独审查接口、控制范围和测试结果，并与正式发行包分离；普通 Mod 运行不依赖它。

## 更换模型时的开场指令

```text
先完整读取 RULES.md、HANDOFF.md、README.md，检查当前分支、工作区及本机环境。
按 HANDOFF 的下一步继续，只做当前阶段授权范围内的工作。
每次建设后更新 HANDOFF，并与对应变更一起提交；明确实际测试与未验证项。
```

这是给无法自动发现模型入口文件的客户端使用的补充；共同事实始终保存在仓库里。
