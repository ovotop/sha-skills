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
