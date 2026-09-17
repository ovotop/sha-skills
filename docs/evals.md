# 评估说明（sha-plain-talk / sha-plain-docs）

本文件说明两个 skill 的评估怎么做的、结果如何、哪些地方偏离了 skill-creator 的标准流程、以及已知限制。
评估**运行数据不随仓库提交**（工作区是仓库外的兄弟目录），本文件是可追溯的说明与结论。

## 运行数据位置（仓库外）

| 内容 | 路径 |
|---|---|
| talk 评估工作区 | `../sha-plain-talk-workspace/iteration-{1,2}/` |
| docs 评估工作区 | `../sha-plain-docs-workspace/iteration-{1,2,3}/` |
| 每用例的期望与证据 | `<workspace>/iteration-N/eval-<id>-<name>/{eval_metadata.json,with_skill/run-1/grading.json,without_skill/run-1/grading.json}` |
| 机械评分（脚本直跑） | `<…>/<config>/grading-mechanical.json` |
| benchmark（官方脚本产出） | `<workspace>/iteration-N/benchmark.{json,md}` |
| 触发评估 | `<workspace>/iteration-1/trigger-report.json` |
| 逐用例观察与迭代依据 | `<workspace>/iteration-1/findings.md` |

## 方法

- 用例定义：`skills/<name>/evals/evals.json`（各 6 例，含针对"事实来源/置信阶梯、黑话、结论先行"的定向用例）。
- 每例跑 **with_skill 与 baseline 两个配置**（配置间模型一致；429 后统一降级到同一 fallback 模型）。
- 评分为两层：**机械层**＝`check_plain.py` 直跑输出（句长、禁词/黑话、指代、强断言来源标记、删改对比）；**语义层**＝LLM judge 按 `skills/<name>/evals/rubric.md` 逐项判 PASS/FAIL 并附证据。
- 汇总用 skill-creator 的 `scripts/aggregate_benchmark.py`。

## iteration-1 结果（12 例 × 2 配置 = 24 运行）

| skill | with_skill | baseline | delta |
|---|---|---|---|
| sha-plain-docs | **98.5%** | 63.5% | **+0.35** |
| sha-plain-talk | 83.3% | 90.5% | **−0.07** |

机械层对照（`check_plain.py` 违规数，with_skill vs baseline）：docs eval-1 `0 vs 18`、eval-2 `0 vs 22`、eval-4 `0 vs 91`；talk 多数用例违规来自技能自身措辞缺陷（见下）。

**talk 出现负 delta 的原因（已修复）**：5 处缺陷全部来自 skill 自身措辞，而不是模型能力——
1. 输出模板"细节与例外附在最后"诱导模型追加 `细节：…` 尾段（6 例中 5 例出现），既复述首句又构成元注释；
2. 自检第 ④ 项缺少 `相关`/`该` 的示例，导致 `相关信息`、`该接口` 漏检；
3. 内核表句长行只写了"无逗号单句 ≤40"，漏掉 `docs/rules.md` 的"**总长超 40 一律违规**"；
4. 黑话替换时把 `抓手` 整词丢掉（丢信息，违反"保留事实"）。

**docs 的唯一缺陷**：eval-3 的小节标题仍是名词标签（「变更内容」「使用限制」）——两个配置都 FAIL。

## iteration-2 / iteration-3（修复验证）

只复跑受修复影响的用例（**偏离**：skill-creator 要求每轮全量复跑；此处复用 iteration-1 的 baseline，因为 skill 的改动不影响无技能配置）：

| 用例 | iteration-1 | iteration-2/3 | 结论 |
|---|---|---|---|
| talk eval-1 结论先行 | 1 违规 + 元注释 | **0 违规** | 模板修复生效 |
| talk eval-2 无来源断言 | 1 违规（`该接口`） | **0 违规** | 指代修复生效 |
| talk eval-4 黑话 | 1 违规 + 丢 `抓手` | **0 违规**，`抓手→切入点` | 信息保留修复生效 |
| talk eval-5 长句/指代 | 5 违规 | **0 违规** | 句长规则 + 模板修复生效 |
| talk eval-6 英文 | 元注释 | **0 违规**，单段 | 模板修复生效 |
| docs eval-3 改写保警告 | 标题标签（两配置都 FAIL） | **0 违规**，标题为判断句、限制保留、`--source` 抓到并修复 `dropped_warning` | 护栏修复生效（iteration-3 为无提示的干净复跑） |

## 触发评估（替代 skill-creator 的 `run_loop.py`）

**偏离原因**：`run_loop.py`/`run_eval.py` 依赖 `claude -p`，本环境无 `claude` CLI。改为**单次批量判断**：给 judge 每条 skill 的 `name + description`（模拟 `<available_skills>`）与 `evals/trigger-queries.json`，逐条判"会不会自动触发"。

| skill | 准确率 | 结果 |
|---|---|---|
| sha-plain-docs | **20/20** | 10 应触发全部命中，10 近邻反例全部正确拒绝 |
| sha-plain-talk | **9/10** | 唯一误触发＝「没听懂，你能讲清楚点吗？」 |

**已知限制（平台差异，未消除）**：talk 的 description 已按 mattpocock 的 user-invoked 约定改为"人面向、无触发词"，但「没听懂，讲清楚点」在语义上仍与描述匹配。
- Claude Code：`disable-model-invocation: true` 生效，模型无法调用，描述也不进上下文 → 不触发。
- OpenCode：**该字段不被支持（只解析 `name`/`description`）**，因此模型仍可能自动调用本技能。
- 这是 wait-what 同样存在的暴露面（其描述同样会被"没听懂"命中）；OpenCode 无 per-skill 开关，`permission.skill: deny` 会连用户调用一起禁掉，故**接受并记录**，不做机制强制。

## 其他偏离记录

- **未跑 eval-viewer**（用户确认精简收尾）：`generate_review.py` 需要浏览器/静态 HTML 评审页；结果直接以 benchmark + 本文件呈现。
- 未做第三轮迭代：边际收益递减（iteration-2 发现的新缺陷"标题复述正文"已用 1 行修复 + 1 次干净复跑验证）。
- 1/24 运行（docs eval-6 with_skill 首跑）产出空文件，属**评测基础设施失败**，已重跑，非 skill 缺陷。

## followup（2026-09-16，change `sha-plain-skills-followup`）

归档后复盘处置了 4 个遗留问题：

| # | 问题 | 处置 |
|---|---|---|
| P1 | check_facts 把规范型情态（必须/不得/禁止）误报为无来源强断言 | **拆出 `normative_modality` 类别，默认告警（warning）**；事实型词表（一定/绝对/必然/肯定/确定…）保持硬查。用户拍板。需 spec 级变更（`sha-plain-skills-followup`） |
| P2 | talk 在 OpenCode 下无机制保证"仅用户触发"（唯一误触发「没听懂，讲清楚点」） | **用户 2026-09-16 拍板：沿用 wait-wait 模式，不做 ClaudeCode/OpenCode 特殊处理**。`disable-model-invocation` 保留（Claude Code 一等支持），description 保持人面向无触发词；OpenCode 无法机制强制，接受暴露面。归档 change 为历史快照不改动，本决定记录在此 |
| P3 | iteration-3 残留：标题已判断句化，但出现"空壳引导句 + 标题回显" | 结构护栏④扩展：空壳引导句（"如下/以下"式）禁用 + 标题已给判断时正文不复述标题（直接写依据/条件/操作/后果） |
| P4 | eval 期望措辞过严：`invalid configuration entries` 是正常形容词 | docs eval-6 期望改为"bare 状态标签单独成句才算违规"（talk eval-6 同款修正）；新增 talk eval-7「未新增事实」定向用例（对应 eval-4 iteration-2 凭空出现"产品"的缺陷） |

复跑结果（iteration-4，with_skill 单配置，复用 iteration-1 baseline——护栏/期望改动不影响无技能配置）：

| 用例 | 机械层（check_plain.py） | 语义层（docs rubric 逐条核） | 结论 |
|---|---|---|---|
| docs eval-3 改写保警告 | exit 0，**0 violations**（1 条 `normative_modality` warning 为 P1 预期）；`--source` 删改对比无 dropped_warning | 核心三问过；护栏①②④过——标题=判断句、无空壳引导句、无条目复述标题、两条限制保留 | **P3 修复验证通过**（iteration-3 的"空壳引导句+标题回显"残留未再出现） |
| docs eval-6 错误提示 | exit 0，0 violations（绿场 `--greenfield`，0 warnings） | `Invalid parameter: 400` 仅作为原消息引用，输出为展开模板（参数名+错误码+下一步），无「无效的参数」机械直译 | **P4 期望修正验证通过**（bare 标签单独成句才算违规的新边界成立） |

**触发面影响**：P1 让改写场景的规范句（"用户必须配置超时时间"）不再被迫加来源标记；"警告/限制/例外保护性保留"与 `--source` 删改对比不受影响（D-F-1 边界：新增要求的语义层兜底不变）。

## 触发再设计（2026-09-17，「你说啥」触发 talk）

**背景**：触发评估（iteration-1）显示 talk 唯一"误触发"＝「没听懂，你能讲清楚点吗？」，当时沿用 user-invoked 模式接受该暴露面（P2）。但 OpenCode 不解析 `disable-model-invocation`，用户实际说「你说啥」时模型本就会自动调用本技能——旧设计等于"默认行为 vs 文档声明"不一致。

**新决策（用户拍板）**：把自然语言困惑短语从"暴露面"转为**设计内触发**：

- **talk**：移除 `disable-model-invocation: true`（Claude Code 侧不再拦）；description 新增触发词「你说啥」「没听懂」「没明白」「什么意思」「再说一遍」「没看懂/没看清」，并对「重新回答一遍」「这次用英文」等重做/语言切换请求显式排除；正文触发规则改为"显式调用 **或** 困惑短语 → 进入重讲"，**新问题/新请求仍不进入**。
- **docs**：description 扩充触发面（README、release notes、错误消息文案、隐式表达如"帮我写个配置说明"），强化自动触发。

**复跑验证（批量判断法，同 iteration-1 方法：给 judge 每条 skill 的 name+description 与 trigger-queries.json，逐条判会不会自动触发）**：

| skill | 准确率 | 结果 |
|---|---|---|
| sha-plain-docs | **20/20** | 10 应触发全部命中，10 近邻反例全部正确拒绝（同 iteration-1） |
| sha-plain-talk | 首轮 **12/13** → 加排除边界后 **13/13** | 首轮近邻误触发＝「重新回答一遍，这次用英文」（语义近触发词「再说一遍」，实为重做/语言切换）；description 补排除句后复跑通过 |

**一致性更新**：`openspec/specs/sha-plain-talk/spec.md`《触发重讲》改写（自然语言困惑自动路由替代"不被自动路由"，非重讲场景补重做/语言切换反例）；`trigger-queries.json` 翻转 1 条反例并新增 3 条正例；README 表格与使用段落同步；`docs/evals.md` 追加本记录。
