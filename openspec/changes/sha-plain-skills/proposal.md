## Why

本仓库的 AI 输出（对话回复、技术文档）默认偏向冗长、官腔、黑话堆积，与"一次读懂、准确执行"的表达目标相悖。现有方法（docs/rules.md 的中文受控写作框架、金字塔原理、ASD-STE100 方法论）散落在文档中，但没有任何机制**在生成时强制执行**，导致每次都要靠人工提醒。本 change 将这套方法论固化为两个可被高频触发、接近零常驻上下文的 Agent Skills，让"清晰表达"从主观意志变成可复现的默认行为。

## What Changes

- **新增 `sha-plain-talk` skill**：对话场景的"重讲"技能。用户触发（`disable-model-invocation: true`），在上一条消息没讲清时，按金字塔结论先行 + 受控写作内核重新表达。全内联、零 references、体积预算 ~30-40 行。
- **新增 `sha-plain-docs` skill**：文档写作技能。模型可自动触发（按任务类型），支持中/英目标语言切换，工作流 = 金字塔结构 → 微观规则 → lint 脚本验证。正文预算 ~100 行，完整规则目录下沉 references/。
- **新增 `scripts/check_plain.py`**（docs skill 内置）：确定性 lint，检查句长上限、禁用词/黑话命中、情态词篡改（may≠must），供评估与生产复用。
- **新增 `references/` 规则目录**（docs skill）：`rules-zh.md`（中文受控写作全表，单一事实源 docs/rules.md 复制并标注来源）、`rules-en.md`（精简 STE 英文规则）、`avoid-words.md`（完整黑话清单，talk 内联其 top-15 子集）。
- **新增 `.gitignore`**：忽略 `conversations/`（会话插件数据目录）。

**不改动** `docs/rules.md`（保持单一事实源身份），**不引入**中英对照双语配对模式（已确认无场景）。

## Capabilities

### New Capabilities

- `sha-plain-talk`: 对话重讲技能。用户触发时按"结论先行 + ≤3 点论据 + 短句 + 无黑话 + 明确指代"重新表述上一条未讲清的消息，中英文均可。
- `sha-plain-docs`: 受控文档写作技能。按目标语言（zh/en）应用金字塔结构与中文受控写作（或精简 STE）规则，输出可经 check_plain.py 确定性验证。

### Modified Capabilities

（无现有 spec 变更——本仓库尚无既有 capabilities）

## Impact

- **仓库**：`sha-plain-skills` 仓库新增两个 skill 目录 + lint 脚本 + .gitignore。
- **触发面**：`sha-plain-talk` 用户触发（零常驻上下文）；`sha-plain-docs` 模型可自动触发（description 常驻，预算 <60 词）。
- **依赖**：无新增运行时依赖；`check_plain.py` 仅用标准库 Python。
- **约束**：规则知识密度决定放置位置：金字塔原理（模型权重强）→ leading word 内联；中文受控写作框架（模型无此知识）→ 必须携带 references/；量化阈值 → 携带 + 脚本验证，不靠记忆。