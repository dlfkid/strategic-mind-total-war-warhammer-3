# API 验证记录

初建日期：2026-10-14。来源编号见 [来源表](sources.md)。所有实机结果目前都是 `NOT_RUN`，实际游戏构建未知。接口原名是后续检查清单，不是可直接复制执行的已验证代码。

## 如何记录证据

| 等级/状态 | 定义 |
| --- | --- |
| `DOC` | 查到接口说明或候选机制，尚未对照用户安装 |
| `SOURCE` | 核对了明确版本的文件；必须写明是镜像、第三方 schema 还是实际游戏文件 |
| `GAME / PASS` | 指定游戏构建内完成实验，并有读回或行为结果证据 |
| `NOT_RUN` | 尚未执行实机实验，不能理解为失败或通过 |
| `FAIL` / `INCONCLUSIVE` | 指定实验不符合预期 / 证据不足；保留环境和复现步骤 |

`DOC`、`SOURCE` 是证据来源，不是功能完成度的百分比。没有抛错只能证明该次调用未观察到异常，不能代表策略生效。

## 候选能力

| ID | 能力与准确入口 | 当前证据 | 必须验证的结果 | 实机状态 |
| --- | --- | --- | --- | --- |
| API-01 | Mod 加载；候选入口 `script/campaign/mod/sm_probe.lua` | 加载方式待当前游戏确认；S04、S16 仅提供结构背景 | 新局/旧档各一次加载标记，重载不重复注册；核对库与运行时 | NOT_RUN |
| API-02 | `core:add_listener` / `core:remove_listener` | DOC，S08 | 一次真实事件的触发时机、完整上下文与去重；移除后不再触发 | NOT_RUN |
| API-03 | `cm:model():world()`、派系/角色/军队/地区接口 | DOC，S04、S07 | 读取选定存档对象；死亡、海上、无领土、空接口时安全返回 | NOT_RUN |
| API-04 | `cm:add_saving_game_callback`、`cm:add_loading_game_callback`、`cm:save_named_value`、`cm:load_named_value` | DOC，S05 | 嵌套基本值表保存→退出→读取一致；缺键使用默认；不重复执行请求 | NOT_RUN |
| API-05 | `character:is_visible_to_faction`、玩家可见角色/地区列表 | DOC，S07 | 已探索但不可见、当前可见、伏击/隐藏及重新失去视野；核对参数类型 | NOT_RUN |
| API-06 | `cm:show_message_event`（初版优先），定位形式后置 | DOC，S05 | 当前合法本地化 key、消息类型索引、历史显示、关闭通知、重载不重复 | NOT_RUN |
| API-07 | `out`、`script_error` | DOC，S09 | 实际输出通道/开关/路径，一行结构化记录可检索，失败记录不静默 | NOT_RUN |
| API-08 | `cm:cai_strategic_stance_manager_set_stance_promotion_between_factions_for_a_given_stance` | DOC + SOURCE（文档镜像），S06 | 在限定回合窗口设置、读回起止与当前值，到期后无残留；行为另记 | NOT_RUN |
| API-09 | `cm:force_change_cai_faction_personality`、`cm:cai_set_faction_script_context`、`cm:cai_get_faction_script_context` | DOC + SOURCE（文档镜像），S06；性格表 SOURCE（schema），S14 | 当前 DB key 有效，单变量读回/行为差异，原版是否覆盖及如何恢复 | NOT_RUN |
| API-10 | `cm:cai_disable_movement_for_character` / `cm:cai_enable_movement_for_character`，配合 `cm:move_to` / `cm:attack` | DOC + SOURCE（文档镜像），S06；命令封装 S05 | 单 AI 军团合法移动/攻击、失败/超时反馈、重载恢复、归还后原版继续行动 | NOT_RUN |
| API-11 | `cm:force_diplomacy`、`cm:force_declare_war`、`cm:force_make_peace` | DOC，S05、S06 | 限制选项与实际外交状态分别检查；联盟连锁与人类影响另测 | NOT_RUN |
| API-12 | `cm:cai_add_diplomatic_event` | DOC + SOURCE（文档镜像），S06；事件表 SOURCE（schema），S14 | 合法事件 key、方向、叠加、衰减，绑定真实事件；不借不存在的事件改变关系 | NOT_RUN |
| API-13 | AI 模型的 `strategic_stance_between_factions` 与 promotion 读回方法 | DOC + SOURCE（文档镜像），S07 | 从当前模型取得 AI 接口，核对各方法参数/返回值与读回时间 | NOT_RUN |
| API-14 | `cm:war_coordination()`、`WarCoordinationRequestIssued` | DOC，S06、S07 | 区分请求事件、favour 读写和真正下达任务；通用任务分派入口仍未知 | NOT_RUN |
| API-15 | `mission_manager:add_new_scripted_objective`、`mission_manager:set_victory_mission`、`mission_manager:set_victory_type`，候选 payload `game_victory` | DOC，S10；胜利表 SOURCE（schema），S14 | 核对当前任务构造/payload，脚本目标、正式胜利、重载进度分别验收；Steam 成就单独测试 | NOT_RUN |
| API-16 | battle setup 加载脚本，`unitcontroller:take_control` / `release_control` | DOC，S11、S12 | 普通战役战斗中安全加载，单单位接管和恢复，自动战斗与攻城不受破坏 | NOT_RUN |
| API-17 | `cm:cai_add_point_of_interest_generic_marker` / `cm:cai_remove_point_of_interest_generic_marker` | DOC，S06 | 核对 DB 的 POI 组响应、编号冲突、作用对象、存档和移除；不能仅凭 marker 存在认定 AI 采取行动 | NOT_RUN |

S06/S07 的 `SOURCE` 表示在固定提交的 HTML 原文件中找到方法，不表示拿到游戏引擎实现。S14 只证明第三方维护的 schema 包含相关表结构。

## 事件上下文检查单

先在实际版本打印受限字段，再写业务逻辑。以下事件来自 S07；继承上下文与返回类型可能未完整列出，不自行补齐。

| 事件 | 用途 | 关键检查 |
| --- | --- | --- |
| `FactionTurnStart` | 选定派系的低频评估 | faction、回合阶段、加载后监听次数 |
| `PositiveDiplomaticEvent` | 结盟/贸易等变化 | proposer、recipient、联盟类别；协议不等于共同作战 |
| `NegativeDiplomaticEvent` | 宣战/毁约等变化 | proposer、recipient、`is_war` 等标志，核对方向 |
| `CharacterSackedSettlement` / `CharacterRazedSettlement` | 米登领真实受袭事件 | character、garrison residence、地区与事件时机；同战斗去重 |
| `CharacterCompletedBattle` | 战后结果及共同参战候选 | character、pending battle、敌我角色/增援信息在回调时是否仍有效 |
| `CharacterFinishedMovingEvent` | 行动后观测候选 | 镜像显式列出 `was_flee`，不能假定角色字段一定可用；回合快照作为备选 |

没有找到标准 `FactionWarDeclared` 事件的文档依据，先使用已列出的外交事件核对。`CharacterDiscovered` 也不能仅凭名称当作某个玩家的视野通知。

## 单次验证记录模板

以下模板尚未填写，不是测试结果。实机执行后将一份记录追加到本文件，过多时再按实验拆文件。

```text
experiment_id / api_ids:
run_id / date / tester:
platform / storefront / game_version / build_id:
mod_commit / package_hash / schema_commit:
campaign / save_hash / turn / difficulty / dlc / mod_load_order:
local_source_paths_and_hashes:
prerequisites / steps / exact_arguments:
expected_readback / expected_world_effect / timeout:
actual_return / actual_readback / observed_events:
player_visibility_before_and_after:
cleanup / control_restored / save_reload_result:
result: NOT_RUN | PASS | FAIL | INCONCLUSIVE
evidence_paths / limitations / next_action:
```

引用日志或截图时放在本地 `artifacts/`，提交可复核的摘要和哈希；不要将私人存档或海量游戏数据直接加入仓库。API-08 的 promotion 读回通过与军队行为改变必须分别记录，API-10 的命令观测通过与自主规划能力也分别记录。
