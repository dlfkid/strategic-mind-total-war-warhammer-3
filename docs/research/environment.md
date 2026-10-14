# 本地环境与验证边界

记录日期：2026-10-14（Asia/Taipei）。这些是本次实际执行的盘点，不代表扫描了整台机器或其他远程主机。

## 已确认

| 项目 | 结果 |
| --- | --- |
| 工作目录 | `/Users/seal/Documents/coding/strategic-mind-total-war-warhammer-3` |
| Git | 已有仓库，主检出，分支 `main`，初始提交 `c4987fa` |
| 初始化前文件 | 仅 `LICENSE`，MIT，原始工作区干净 |
| 远端 | `https://github.com/dlfkid/strategic-mind-total-war-warhammer-3.git`，默认分支 `main` |
| GitHub CLI | 可用，当前登录账户可读取该仓库和公开工具仓库；不记录凭据 |
| 宿主平台 | macOS；本次在当前目录原地工作 |
| Lua / RPFM | `command -v lua`、`command -v rpfm` 没有返回路径，未发现 PATH 中的对应命令 |
| 网络调查 | 已访问官方公告、CA 文档镜像、RPFM 发布与 schema，详见 [来源记录](sources.md) |

## 查找过的安装位置

- `/Applications/Steam.app`
- `/Users/seal/Library/Application Support/Steam/steamapps`
- 当前仓库相邻的 `Total War WARHAMMER III` 目录
- `/Volumes/SANDISK/SteamLibrary/steamapps` 和 `/Volumes/SANDISK/steamapps`
- `/Volumes/TOSHIBA EXT/SteamLibrary/steamapps` 和 `/Volumes/TOSHIBA EXT/steamapps`

上述常见位置均未发现相应安装。两个外置卷存在，但未递归检查所有目录；游戏、Steam、Assembly Kit 或 RPFM 可能位于其他路径或另一台电脑。不能由此断言用户没有安装或拥有游戏。

## 未取得的条件

实际游戏版本、Steam Build ID、当前 `data/*.pack`、Assembly Kit 原始定义、原版 campaign Lua、派系/角色/地区 DB key、可运行战役、测试存档、日志输出路径和任何游戏内观测。

因此，当前所有游戏 API 实验结果均为 `NOT_RUN`。未进行 `.pack` 制作、游戏启动、存档往返、AI 行为测试、消息渲染或成就测试。文档中关于这些能力的结论均限于资料或第三方 schema。

## 下一次环境接入

在实际测试机上先记录：操作系统与游戏平台、主菜单版本、Steam 的 `appmanifest_1142710.acf` 中 Build ID（适用时）、DLC、活动 Mod 及加载顺序、语言、战役/战斗难度、测试存档回合和硬件。不要把 Build ID 与公开补丁号混为一谈。

从该安装读取相关包与脚本，原始导出放 `local/`；可提交的是路径清单、文件哈希、必要的小片段和结论。默认不提交原版大文件或个人存档。RPFM 当前发布资产为 Windows/Linux，macOS 上不假定可直接运行其二进制，也不自动安装虚拟机或兼容层。
