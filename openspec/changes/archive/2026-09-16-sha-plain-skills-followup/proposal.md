## Why

2026-09-16 归档的 sha-plain-skills 遗留 4 个问题（详见归档 design 的"评估结果"与 docs/evals.md）：

1. **check_facts 对规范型情态误报**：`必须/不得` 是规范要求（操作手册/API 说明里的正常表述），却与事实型强断言（一定/绝对/必然/肯定…）共用硬查，导致改写场景的规范句被迫加来源标记。用户已拍板：拆出 normative 类别，默认告警。
2. **P3 结构残留**：标题=判断句修复后，`iteration-3/eval-3` 输出仍出现"空壳引导句 + 标题回显"（"本次更新的变更与使用限制如下。"→"本次更新优化了性能。"）。结构护栏④未覆盖"如下/以下"式引导句。
3. **P4 期望措辞**：docs eval-6 期望"不得原样堆机械状态词（如 invalid）"过严——`invalid configuration entries` 是正常英文形容词。
4. **P2 平台差异已确认接受**：用户确认 talk 沿用 wait-what 模式（OpenCode 无法机制强制仅用户触发，记录即可，不做特殊处理）。

## What Changes

- **check_plain.py**：把强确定性词词表拆为**事实型强断言**（一定/绝对/必定/必然/肯定/显然/无疑/确实/确定/从不/总是/永远；en：always/never/definitely/certainly/obviously/proven）与**规范型情态**（必须/不得/禁止；en：must）两类；规范型命中默认告警（warning）而非违规（violation），不再要求来源标记。
- **docs spec《确定性验证》**：第 2 条拆出 normative_modality 类别，明确规范型情态默认告警。
- **docs spec《金字塔结构》**：护栏④扩展——空壳引导句（"如下/以下"式）列入禁用项。
- **talk spec《输出前自检》**：自检项②措辞同步区分"事实断言 vs 规范要求"：规范型情态（必须/不得）不需要来源标记，但"警告/限制/例外仍保护性保留"。
- **两个 SKILL.md + 两个 rubric**：置信阶梯措辞区分事实断言与规范要求。
- **docs evals.json eval-6**：期望放宽（bare 状态标签单独成句才算违规，正常形容词不算）。
- **docs SKILL.md 结构护栏④**：禁止"如下/以下"式引导句 + 标题已给判断时直接列条目、不复述标题。

**不改动** `docs/rules.md`（单一事实源身份）；**不改动** talk 的触发机制（用户确认沿用 wait-what，仅补 design 记录）。

## Capabilities

### Modified Capabilities

- `sha-plain-docs`：确定性验证/金字塔结构两条 requirement 措辞修订，行为不变（violation 计数规则调整）。
- `sha-plain-talk`：输出前自检措辞修订（区分事实断言 vs 规范要求），行为不变。
- `check_plain.py` 行为变更：`必须/不得/禁止/must 类规范词不再计为 violation（降为 warning）。

## Impact

- **check_plain.py**：词表拆分 + 新 rule 类别，`--json` 报告新增 `normative_modality` 类别；退出码语义不变（warning 不触发 exit 1）。
- **触发面**：无变化（talk 保持用户触发，docs 自动触发）。
- **依赖**：无新增。
- **评估**：docs eval-3 复跑 1 个用例验证 P3 护栏；docs eval-6 期望修正（P4）。