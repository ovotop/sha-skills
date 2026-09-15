# Design: sha-plain-skills

## Context

本仓库是 Agent Skills 集合仓库（`sha-skills`），零现有 skills，`docs/rules.md` 是中文受控写作的方法论源（ASD-STE100 的中文化移植）。动机见 `proposal.md - Why`。

两个新 skill 服务于同一目标——"AI 输出清晰、可执行、无歧义"——但场景不同：

- **sha-plain-talk**：对话。上一条消息没讲清时**重讲**。
- **sha-plain-docs**：文档。写/改任何技术文档时**应用受控写作 + 金字塔结构**。

核心约束（来自探索阶段确认的需求）：

1. **高频使用** → 每次触发 SKILL.md 正文完整进上下文 → 体积压缩是头等目标。
2. **中英文都支持**，目标语言切换，**无中英对照配对模式**。
3. **用户已明确**：不管理分发、conversations/ 目录需 gitignore、docs 带 lint 脚本、黑话清单用 `_Avoid_` 结构。
4. 设计/实现参考 skill-creator 工作流；设计完成并经 Oracle review（第一轮已执行，本版为按 B1–B3 / S1–S7 修订后的复审版）。
5. 参考来源：wait-what（github.com/mattpocock/skills）、danyuchn/asd-ste100-skill、woosal1337/blog asd-ste100、AminBlg/SimpleEnglish、ruanyf/document-style-guide、金字塔原理（结构化思考与表达）。

## Goals / Non-Goals

**Goals**
- SKILL.md 正文按"每次调用计费"压缩：talk ≤ ~40 行，docs ≤ ~100 行，description < 60 词。
- 规则放置遵循"知识强度决定存放位置"原则，但**区分"知道概念"与"默认会做"**（见 D1 修订）。
- talk 零脚本依赖但**含输出前自检清单**（B3 修订）；docs 确定性检查交给脚本而非模型记忆。
- 每个 skill 的 spec MUST 项都有对应的机制承载（内核表/自检清单/脚本/references）——不允许"MUST 无兜底"。
- 支持 skill-creator 量化 evals（句长、禁词、情态；结论先行用 LLM-judge）。

**Non-Goals**
- 不做中英双语对照（aligned bilingual）模式 —— 已确认无场景。
- 不构建仓库级 CONTEXT.md 依赖 —— 对话场景无仓库上下文；黑话清单内嵌替代。
- 不管理分发/上传流程（用户明确"不用管"）。
- v1 不做"核心 + 双壳"（mattpocock 式共享核心）架构 —— 复杂度压到 v2，若漂移成为现实问题再升级。

## Decisions

### D1. 知识强度决定规则存放位置（第一性原则 · 已按 Oracle S1 修订）

**决定**：按"模型权重中的知识强度 + 默认行为的可靠度"双轴分级放置规则。核心修正：**"知道概念" ≠ "默认会做"**——知识强度只决定要不要教，行为可靠度才决定要不要约束。

| 知识维度 | 声明性知识 | 默认行为可靠度 | 处理 |
|---|---|---|---|
| 金字塔原理口号层（结论先行/MECE/SCQA） | 极强（商业经典） | **中：术语都会说，输出不稳定**（MECE 分组重叠/不穷尽是高频失败点） | 内联**结构微模板**（结论先行→≤3 支撑→细节）+ 4 条结构护栏，**不建 pyramid.md** |
| 金字塔操作层（SCQA 变体/序言≠摘要/标题=判断句等） | 强 | **低：半记得、常做错** | 4 条单行护栏内联入 docs 正文；SCQA 变体映射作 rules-zh.md 的 3-4 行附录 |
| 英文 STE 核心规则 | 强（wait-what 已证明） | 短输出中；**长输出必漂移** | talk/dactory 短输出走触发 + 两三条护栏；docs 长输出 v1 允许"方向性"级，**设升级阈值**（D8） |
| 中文受控写作框架 | 弱（无系统训练语料，半记得阮一峰碎片） | 低（默认官腔+黑话方向相反） | **必须携带** references/rules-zh.md + **读取机制**（S3 修订） |
| 量化阈值（40 字/20 字子句/「」/混排空格/禁该其此） | 碎片 | 不可靠 | 携带 + `scripts/check_plain.py` 双层验证（S5 修订） |
| 黑话清单（赋能/抓手/闭环） | **数据不是知识** | 模型主动偏好产出 | 必须携带 avoid-words.md（talk 内联 top-15 子集） |

**理由**：wait-what 8 行成立的前提是（a）英文 STE 知识扎实 **且**（b）输出极短可维持模式。本设计两个 skill 都缺一个前提：talk 是中文（默认方向是官腔）、docs 是持续长输出（口头模式必漂移）。修订要点：**不因"模型知道金字塔"就放弃约束**——知道 ≠ 输出即符合，MECE 反例为证；但也不需要建完整 pyramid.md——结构微模板 + 结构护栏已覆盖高频失败点。

**备选**：
- wait-what 式全裸 → 否决：中文官腔默认方向 + 金字塔行为不可靠，双重理由。
- 全量携带（含 pyramid.md） → 否决：口号层模型真会（结论先行/SCQA 词汇无碍），携带纯浪费上下文；操作层用 4 条护栏精装捕捉。

### D2. 架构：两个独立 skill（A 方案），语言切换进 references

**决定**：`sha-plain-talk` 与 `sha-plain-docs` 各自独立、自包含；语言（zh/en）是 skill 内部的一个维度，通过 SKILL.md 的"目标语言 → 选 references"工作流切换，不产生 `*-zh` `*-en` 变体 skill。

**理由**：
- 方法论语言无关（金字塔），只有微观规则分语言（40 字 vs STE）→ 拆语言变体会被迫复制共享部分，制造漂移源。
- skill-creator 原生模式就是"变体进 references"（cloud-deploy/SKILL.md + aws.md/gcp.md 先例）。
- 触发不分裂：docs 一个 description 覆盖"写中文或英文文档"全场景。

**备选**：
- B（单 skill 双 register）→ 否决：对话与文档触发粒度太粗，两者要分担一个 description，触发精准度下降。
- C（核心 skill + 双壳 router）→ v2 预留：零重复 + 触发精准兼得，但 v1 复杂度最高，且 cross-skill "Call the Skill tool with X" 在 OpenCode 的支持度未验证。

### D3. 触发模式：两 skill 故意不同（已按 Oracle B2 修订调用面）

**决定**：
- `sha-plain-talk` → `disable-model-invocation: true`（**仅用户显式触发**）。"上一条没讲清"是只有人类能判断的条件。**真实调用面 = 用户显式点名 / slash command**；自然语言"讲清楚点"不路由到本 skill（disable-model-invocation 语义如此，见 B2 修订）。副产品：零常驻上下文。
  - ⚠️ **平台能力待实测**（tasks 加 smoke test）：`disable-model-invocation` 字段名、slash command 注册、OpenCode 支持度——在 SKILL.md 落地前用 smoke test 验证，不当作已定事实。
- `sha-plain-docs` → **模型可自动触发**（省略该字段）。"写文档时该用受控结构"是模型可判断的任务类型。代价：description 常驻 → 压到 <60 词。
  - **双重分类风险显式化（S4）**：自动触发后**两层分类都要做对**——(a) 是不是文档任务？(b) 是哪种适用强度？正文第一步 MUST 做显式判定，拿不准问用户；两层各配一个 eval 用例。

**理由**：mattpocock invocation 决策规则："Pick model-invocation only when the agent must reach the skill on its own… If it only ever fires by hand, make it user-invoked and pay no context load."

### D4. 压缩范式：微观内核表 + 自检清单 + 结构护栏（已按 Oracle S2 / B3 / S2 修订

**决定**（修订后）：
1. **内核表**内联在两个 SKILL.md 正文，按 **通用 / zh / en 标注适用域**（S2 修订）：

```
结论先行            [通用] 首句结论 → ≤3 支撑 → 细节后置
保留事实            [通用] 置信阶梯：有来源→强语态；无来源推测→弱语态；不可判→删除
一词一义            [通用] 不轮换同义词；禁黑话/机械直译
显式主语+主动语态    [通用] 一句一义，执行者明确      ← 新增（对齐 talk spec）
避免模糊副词        [通用] 非常/特别/基本上等        ← 新增（对齐 talk spec）
≤40 字              [zh]   无逗号单句 ≤40 字；30-39 字需语义明确
短句+主动           [en]   英文护栏                  ← 新增（B3：英文 talk 有载体）
明确指代            [通用] 禁"该/其/此/上述/相关"
```
2. **talk 加"输出前自检清单"**（B3：talk 零脚本，用 5 项可勾选自检兜底）：
   - 结论在首句？无来源强断言已加来源/降级/删除？无黑话？指代可定位？单句 ≤40 字（zh）？
3. **docs 加 4 条结构护栏**（S1 + 金字塔操作层，单行，每条 ≤15 字）：

```
序言=提示已知 | 标题=判断句非标签 | 归纳优先不混用 | 空壳句禁用（"存在N个X："）
```

**理由**：danyuchn/asd-ste100 先例（正文 10 行表 + 6 项扫描清单，53 条全量 references）。修订目标：**每个 spec MUST 项都有机制承载**——S2 修订补齐了缺失项，B3 修订给了 talk 最低兜底。

### D5. 事实来源双层检查：脚本管结构，人管语义（已按最终共识修订：置信阶梯 + 来源标记）

**决定**：docs skill 内置 `scripts/check_plain.py`（标准库 Python）。工作流：`写 → 跑脚本 → 修`。

检查分两层（对应"主观判断 vs 客观事实"的可检查性边界）：

| 层 | 查什么 | 谁查 | 机制 |
|---|---|---|---|
| **结构层** | 强断言**有没有**带来源标记 | 脚本（check_facts 逻辑） | 模式匹配：扫描强确定性词（一定/必须/绝对/必定/必然/肯定/显然/无疑/确实/确定/从不/总是/永远），检查所在句或**紧邻前句**是否含来源成分（根据/依据/据/来自/显示/表明/报告/文档/监控/日志 + 来源实体，或（）内标注）。**无需 --source**；"确认"不得单独作来源标记（需与明确来源主语连用） |
| **语义层** | 来源真不真实、支不支持结论、绿色场景强断言是否合理 | 在场的人（对话）/ LLM-judge（评估期） | 判断——脚本只报告不阻塞 |

- 结构层规则：**有可核对来源上下文的断言（改写/重讲/引用场景）无来源标记 = 硬性违规**；**绿场写作（无原稿）强断言降级为告警**，交语义层（S6 的 LLM-judge rubric）判定。
- **`--source` 模式仅保留给"删改方向"**（改写场景对比原文，检测显式警告标记词如"仅/不得/除非"缺失）——best-effort，不宣称能检测语义性删除。
- 句长双层检查（S5）：句子级（无逗号 ≤40 字，30-39 字"需确认语义"）+ 逗号子句级（构件 ≤20 字），与 rules.md 原规则一致。
- 黑话检索读取 avoid-words.md（机器可读行格式，D-defer-3）。
- 标点/空格检查（「」、全角、中英文间空格）。`--json` 输出 + 退出码约定。

**理由**：
- 模型做确定性检查又慢又贵又不准；脚本快准可复用，同时服务 evals 与生产。
- 关键转折（对应 Oracle B1）：**机械检查"情态变没变"不可行（需 diff 且误伤合法升级）；改为检查"强断言有没有来源"**——结构性的、脚本可靠、无需原稿。语义真实性留给在场的人与 LLM-judge。
- 绿场/改写场景区分（Oracle B2）：改写场景"来源"边界可核对（原稿即参照系），结构层可硬查；绿场写作"依据"含模型稳定知识，机械判不了，降级告警交由语义层——避免破坏"写一篇 API 说明"这类无原稿任务。

### D6. 单一事实源与复制策略（已按 Oracle S6 修订）

**决定**：`docs/rules.md` 保持唯一事实源；`references/rules-zh.md` 为物理复制 + frontmatter 注明 `Source: docs/rules.md`，**新增内容隔离到"## 本 skill 新增"节（混排标点、SCQA 变体映射等）**，与复制内容明确划分（S6）。**tasks 加 drift-check 任务**（diff 或 lint 门禁）：`docs/rules.md` 变更时强制同步 references/rules-zh.md，不再空口"靠 review"。

**理由**：skill 安装后必须自包含；mattpocock 的 cross-skill 依赖约定（"Call the Skill tool with X"，禁止 `../sibling/FILE.md`）不适用于普通 skill 孤岛。明确承认 v1 有刻意分叉（新增节），用 drift-check 管理而非否认。

### D7. 文件结构终稿（修订版 · 2026-09-15 实现期布局修订）

**布局修订（实现期，用户确认）**：skill 落地在 git 追踪的 `skills/<name>/`，并从 `.claude/skills/<name>` 建**相对符号链接** `../../skills/<name>`。理由：与仓库既有的 skill-linker 约定及 15 个兄弟仓库（ezk / whitebox-tracking / mi-skills 等）一致；`.claude/skills/` 同时被 OpenCode 与 Claude Code 读取，D3 的 smoke test（2.1/2.2）才能真实执行。**否决**：仓库根目录直放（不在任何发现路径上，无法验证触发）、`.opencode/skills/`（OpenSpec 插件生成目录，按惯例整体 gitignore，无 diff 历史且无法发布）。

```
skills/sha-plain-talk/     # 用户显式触发 · ~40 行 · 无 references 无脚本
├── SKILL.md               # 工作流 + 内核表(含en护栏) + 5项自检清单 + 置信阶梯+来源标记(D9) + 输出模板 + when-not-to + 黑话 top-15 内联
└── (无 references)

skills/sha-plain-docs/     # 模型可自动触发 · 正文 ~100 行
├── SKILL.md               # description(<60词) + 工作流(判类型选强度→目标语言→结构护栏→微观规则+置信阶梯→跑脚本) + 内核表
├── scripts/
│   └── check_plain.py     # 确定性 lint：句长双层/黑话/强断言来源标记(check_facts, 无需--source)/删改对比(--source, best-effort)/标点
└── references/
    ├── rules-zh.md        # 中文受控写作全表（Source: docs/rules.md + "本skill新增"节含SCQA变体映射）
    ├── rules-en.md        # 精简 STE 方向性规则（结构护栏 + 情态 + 短句）
    └── avoid-words.md     # 完整黑话清单（行格式可机器读取；talk 内联其 top-15 子集）

.claude/skills/sha-plain-talk -> ../../skills/sha-plain-talk      # 两个相对符号链接，随 git 追踪
.claude/skills/sha-plain-docs -> ../../skills/sha-plain-docs
```

### D8. 英文规则扩充阈值（可延期项，明确触发条件）

**决定**：v1 `rules-en.md` 只带方向性护栏；**当"英文长文档任务占比 > 30%"时升级**为扩充实版本（含 53 条精简映射 + 词表）。阈值写进 tasks 的收尾检查。

### D9. 事实来源纪律：置信阶梯 + 来源标记（语义安全的第一原则）

**决定**：为区分"主观判断"与"客观事实"、并确保客观事实有可核对依据，所有输出（talk 与 docs 共用）遵循三级置信阶梯：

```
有依据事实    → 强语态（一定/确认）     ← 客观事实；对话/文档来源入句，模型稳定知识不强加标记
无依据·能定性 → 弱语态（可能/据我判断） ← 主观判断：明示推断性质
无依据·不可判 → 删除                   ← 禁止伪装成事实
```

**"依据"＝对话内可核对来源 **或** 模型稳定知识**（Oracle B2 修订）：tier1 的"来源入句"仅当存在可核对的对话/文档来源时执行；模型稳定知识（如"Docker 默认使用 overlay2 驱动"）不强制加来源标记，避免破坏 docs 绿场写作。**警告、限制与例外为保护性类别，覆盖置信阶梯**（Oracle S5）：无论有无依据，MUST 保留（可弱化语态，不得删除）。

**来源标记语法**（只在增量声明处标注，原样转述不加，保持输出自然）：

| 来源类别 | 句内标注示例 |
|---|---|
| 用户消息 / 对话 | （你上一条消息）（你之前提到） |
| 上文已确认 | （上文已确认） |
| 文件 / 工具输出（repo 场景） | （来自 logcat）（引用 crash log） |

**理由**：机械拦截"情态变没变"会误伤合法升级——用户提供新证据后收紧语态是**正确行为**。判据从"变了没"改为"**没证据却变硬了**"。"保留事实"的红线本质是"只输出有依据的内容"——有依据的升级=事实，无依据的升级=篡改。此决定是 D5 结构层检查（强断言必须有来源）的语义层配套：脚本保证"带没带标记"，本原则保证"标记背后有没有真依据"。

**执行**：写入两个 SKILL.md 的写作协议（约 6 行）：每个确定性表述前自问——依据在吗（对话/文档/模型稳定知识）？有且可核对→强语态且来源入句；有但不便标注（模型知识）→可强语态；无依据但能定性为推测→降级弱语态；无依据且无法定性→删除。

## Risks / Trade-offs

- **[中文漂移默认值]** 模型默认技术写作方向 = 官腔 + 黑话 → 缓解：规则携带 + 自检清单 + 脚本兜底，不依赖模型自律。
- **[B1-情态检测能力边界]** 机械检查"情态变没变"不可行 → 缓解：判据翻转——脚本只查"强断言有没有来源标记"（结构层，可靠）；语义真实性交在场的人 / LLM-judge（D5 + D9）。`--source` 仅用于删改方向 best-effort。
- **[B2-调用面认知]** 用户可能不知道 talk 是显式触发的 → 缓解：slash command 注册 + description 写明"当它讲糊时说 /sha-plain-talk"；测试中验证用户路径。
- **[B3-talk 残差风险]** talk 靠自检清单而非硬约束 → 缓解：5 项自检 + evals 定向测"保留事实/情态/黑话"三最弱项；若评估不达标，升级选项：talk 加最小脚本或改文档级。
- **[undertrigger]** docs 自动触发 → 缓解：description 四要素（When/触发词/负触发/文本类型）+ description 优化循环。
- **[双重分类误触发]** docs (a) 是否文档 (b) 哪种强度 register → 缓解：正文第一步显式判定 + 拿不准问用户 + 各配 eval 用例（S4）。
- **[过约束/教条化]** → 缓解：适用强度分级内置 + when-not-to 段。
- **[lint 误报]** → 缓解：句子级/子句级分级（30-39 字"需确认语义"不硬失败），输出 violation 表。
- **[共享内核漂移]** 两个 SKILL.md 各自内联内核表 → 缓解：v2 升级 C 架构统一（D-defer-2）；v1 靠 evals 回归。

## Migration Plan

1. 本 change 交付两个 skill 目录 + 脚本 + .gitignore（忽略 `conversations/`）。
2. 按 skill-creator 流程评估（with-skill vs baseline，每 skill ≥5 用例，结论先行用 LLM-judge），迭代 SKILL.md 正文与 description。
3. 平台 smoke test（disable-model-invocation 字段、slash command、scripts/ 相对执行、--json 退出码）在实现早期执行（D5-B2）。
4. 安装方式未定 → 本地安装即可用；回滚 = 删除 skill 目录，无状态。

## Open Questions

- 无阻塞性问题。可延期项：黑话清单完整词表规模（启动时按需补全）；rules-en.md 升级触发阈值已定（D8）在实现时跟踪；共享内核漂移守卫归 v2 C 架构。