# 调查来源与快照

核查日期：2026-10-14，Asia/Taipei。仅以开发者公告、工具作者仓库和 CA 脚本文档内容作为技术依据。搜索结果摘要只用于发现资料，结论优先核对正文或 GitHub 原文件。

## 来源目录

| 编号 | 来源 | 可证明的范围 |
| --- | --- | --- |
| S01 | [CA：Patch 9.0.3](https://community.creative-assembly.com/total-war/total-war-warhammer/forums/7-patch-notes-amp-announcements/threads/16126-total-war-warhammer-iii-patch-9-0-3) | 官方于 2026-10-09 发布；含任务重载、胜利目标等修正，不证明 Mod API 工作正常 |
| S02 | [CA：Update 9.0](https://community.creative-assembly.com/total-war/total-war-warhammer/blogs/110-total-war-warhammer-iii-update-9-0-release-notes) | 招募历史、任务管理与 AI 行为已有原版调整，实验须重新建立基线 |
| S03 | [CA：Meet Boris Todbringer](https://community.creative-assembly.com/total-war/total-war-warhammer/blogs/107-total-war-warhammer-iii-lords-of-the-end-times-%E2%80%93-meet-boris-todbringer) | 当前鲍里斯的官方背景与新内容，不能沿用早期版本角色假设 |
| S04 | [CA Campaign Index 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/campaign_index.html) | 战役模型、脚本库与 episodic scripting 的关系 |
| S05 | [CA Campaign Manager 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/campaign_manager.html) | 存档封装、移动/攻击封装、外交限制、原版消息 |
| S06 | [CA Episodic Scripting 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/episodic_scripting.html) | AI 性格、态度、上下文、AI 移动接管以及底层状态修改接口 |
| S07 | [CA 事件与模型接口镜像](https://chadvandy.github.io/tw_modding_resources/WH3/scripting_doc.html) | 事件上下文、角色可见性、AI 态度读回、战争协调的已列出接口 |
| S08 | [CA Core 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/core.html#function:core:add_listener) | 事件监听注册与移除 |
| S09 | [CA Script Library Interface 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/global.html#function:global:out) | `out` 等调试输出；不保证零售版默认生成某个文件 |
| S10 | [CA Mission Manager 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/mission_manager.html) | 脚本目标、任务持久化及 `set_victory_type` |
| S11 | [CA Battle Index 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/battle/battle_index.html) | 战斗脚本加载来源及默认脚本位置 |
| S12 | [CA Unitcontroller 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/battle/battle_unitcontroller.html) | 单位接管、命令与归还控制 |
| S13 | [RPFM 作者仓库](https://github.com/Frodo45127/rpfm) 与 [v5.2.0 发布](https://github.com/Frodo45127/rpfm/releases/tag/v5.2.0) | 工具及发布资产；GitHub API 返回发布时间 2026-10-13，仅有 Windows/Linux 资产 |
| S14 | [WH3 schema 固定快照](https://github.com/Frodo45127/rpfm-schemas/blob/19db98acbb8a05beb786996dc377abad07125e6c/schema_wh3.ron) | 作者维护的表结构、表名存在；不包含用户安装中的实际记录或 key |
| S15 | [CA Lua Language 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/lua.html) | 文档记载的 Lua 5.1 语言环境，当前构建仍需核对 |
| S16 | [CA Campaign Script Structure 镜像](https://chadvandy.github.io/tw_modding_resources/WH3/campaign/campaign_script_structure.html) | 原版脚本结构背景；具体 Mod 自动加载入口需检查当前安装与启动实验 |

## 文档年代与证据等级

S04–S12、S15–S16 是社区托管的 CA 生成文档镜像，不是 CA 对 9.0.3 的实时接口保证。核对 GitHub [镜像仓库固定提交](https://github.com/chadvandy/tw_modding_resources/tree/fd75b764a55dbd6279710d977c262a6d8dca1e5d/WH3)：提交时间为 2025-11-02；其中 episodic 页面页脚仍写 `Last updated 7/9/2024 11:45:04 AM`。这里保留原格式，不推断其日/月顺序。爬取日期与仓库更新时间不代表文档对应游戏版本。

本次通过 GitHub API 阅读了该固定提交中的 `WH3/campaign/episodic_scripting.html` 与 `WH3/scripting_doc.html` 原文件。这只能确认镜像确实列出相应接口，不能替代游戏文件核对。

S14 的 schema 提交为 `19db98acbb8a05beb786996dc377abad07125e6c`，提交时间 2026-10-13。本次读取约 11 MB 的 `schema_wh3.ron` 并核对报告列出的表名。schema 的当前性不自动证明其与用户安装的数据库一致。

## 复核规则

后续游戏内结果必须注明游戏版本、平台和 Build ID，引用本地脚本路径、导出表名及实验记录。第三方 Mod 示例可作为待核对线索，不能单凭其 README、标题或宣传认定底层能力可用。本次未将社区讨论、搜索摘要或未实测的执行桥作为通过依据。

未访问成功的个别旧 `totalwar.com/blog` 地址不作为依据；当前版本信息使用 S01、S02 的官方正文。可访问的页面也可能遗漏接口或保留错误，发现上下文/返回类型矛盾时记录为待测，不能自行补齐。
