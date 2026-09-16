# Design: sha-plain-skills-followup

## Context

2026-09-16 已归档 `sha-plain-skills` change（`openspec/changes/archive/2026-09-16-sha-plain-skills/`），两个 skill 已实现、评估、归档、全局安装。归档后的复盘中遗留 4 个问题（P1/P2/P3/P4，详见 proposal），其中 **P2 已由用户拍板确认接受**，本 change 处理 P1（spec 级）、P3（spec 级）、P4（评估数据）三件，并在归档 change 补记 P2 决定。

关键约束：

1. **P1 是 spec 级变更**：docs spec《确定性验证》第 2 条明确列入 `必须` 为强确定性词。拆出 normative 类别必须同步 spec、design、SKILL.md、rubric、脚本，不能只在代码里改。
2. **单一事实源**不涉及：`docs/rules.md` 此刻无改动需求（rules-en.md 由本 skill 新增，P1 只动 check_plain.py 词表与 skill 措辞）。
3. **P3 的证据**：`sha-plain-docs-workspace/iteration-3/eval-3-rewrite-keep-warning/with_skill/outputs/output.md` 的"空壳引导句 + 标题回显"残留（标题已判断句化，但正文仍写"本次更新的变更与使用限制如下。"后复述标题"本次更新优化了性能。"）。

## Goals / Non-Goals

**Goals**

- check_facts 拆出 normative_modality 类别：规范型情态（必须/不得/禁止/must）不再计为 violation，降为 warning，且**不需要来源标记**。
- 结构护栏④扩展：空壳引导句（"如下/以下"式）禁用；标题已给判断时不复述标题。
- 两个 SKILL.md 与两个 rubric 的置信阶梯措辞同步区分"事实断言 vs 规范要求"。
- eval 期望修正（docs eval-6）并复跑 1 个用例验证（docs eval-3）。

**Non-Goals**

- **不**为 talk 的触发机制做任何特殊处理（用户已确认沿用 wait-what 模式：OpenCode 不解析 `disable-model-invocation`，接受其暴露面）。
- **不**改 `docs/rules.md`（单一事实源）。
- **不**重新评估整个 eval 套件（只复跑受影响用例，沿用 iteration-1 baseline，偏离记录到 docs/evals.md）。

## Decisions

### D-F-1. 词表拆分：事实型强断言 vs 规范型情态（用户拍板：拆出 normative 类别，默认告警）

**决定**：check_plain.py 的强确定性词表拆为两组：

| 类别 | ZH | EN | 行为 |
|---|---|---|---|
| 事实型强断言（facts） | 一定/绝对/必定/必然/肯定/显然/无疑/确实/确定/从不/总是/永远 | always/never/definitely/certainly/obviously/proven | 现状不变：改写/重讲场景硬查（无来源=violation），绿场降级 warning |
| 规范型情态（normative） | 必须/不得/禁止 | must | **默认 warning**，不需要来源标记 |

**理由**：
- `用户必须配置超时时间。` 是操作手册/API 说明里的规范要求（作者立场），不是"断言某事实成立"。把它与"系统一定失败"这类事实断言等同要求来源标记，属误报。
- spec 原文（归档 design D5 的"关键转折"）本就只该管"**没证据却变硬了**"的**事实断言**；规范要求没有"证据"概念——它本身即命令（imperative），来源是文档作者/用户需求。
- 规范型情态降级为 warning 后仍**单列类别**（`normative_modality`），保留可观测性；而规范要求的**删除**（`仅/不得/除非` 类警告词丢失）已由 `--source` 删改对比独立覆盖（DROPPED_MARKERS），两个机制互补不重叠。

**边界**：判断依据写进 SKILL.md（"必须/不得 是要求不是断言，不需要来源标记"），防止模型反向误读为"规范要求可以凭空添加"——**保留事实**规则不变：改写场景仍不得新增原稿没有的要求。

**备选**：保持共用词表+模型规避（否决：脚本继续误报，且与 D9 来源标记原则相抵触）；保持硬查但单列类别（否决：治标不治本，规范句仍会被要求加来源）。

### D-F-2. 结构护栏④扩展：空壳引导句禁用（P3）

**决定**：docs SKILL.md 结构护栏 ④ 从"空壳句禁用"扩展为"**空壳句与空壳引导句禁用**"：不写"存在以下 N 个问题：""本次更新的变更与使用限制如下"这类**空壳引导句**；列表条目不复述标题/首句已给出的判断（标题已判断句化时，正文直接列依据/条件/操作/后果）。

**理由**：iteration-3 干净复跑证明标题=判断句修复已生效，但暴露出下一层：模型写"如下："引导句后，用空壳条目复述标题（"本次更新优化了性能。"）——这正是结构护栏当初要消灭的"空壳"形态的变体。

### D-F-3. 置信阶梯措辞同步（两个 SKILL.md + 两个 rubric）

**决定**：置信阶梯在"有依据→强语态"下新增一行（两个 skill 共用）：

```
规范要求（必须/不得/禁止）：是命令不是事实断言，不需要来源标记；但不得把原稿没有的要求写成交叉引用的"事实"
```

- talk SKILL.md 自检② 从"每个强断言（一定/必须/确认…）都能指出来源"改为"每个**事实型强断言**（一定/绝对/确认…）都能指出来源；**必须/不得 类规范要求**不需要来源标记，但不得新增原稿没有的要求"。
- docs SKILL.md 置信阶梯同款新增行。
- 两个 rubric 核心三问第 3 条措辞同步：强语态示例保持事实型词表，`必须/不得 作规范要求时不需要来源，但不得新增原稿没有的要求`。

### D-F-4. P2 决定记录（用户 2026-09-16 拍板）

**决定**：talk 沿用 wait-what 模式，**不做**对 Claude Code / OpenCode 的特殊处理。`disable-model-invocation: true` 保留（Claude Code 一等支持），description 保持人面向无触发词（OpenCode 下无法机制强制，接受暴露面）。此决定已在归档 design D3 有实现，本 change 仅在归档 change 的评估结果段补记"用户 2026-09-16 拍板确认"，不改任何代码。

**理由**：用户明确"就像 wait-what 那样就可以"——wait-what 同样在非 Claude Code 平台无机制保障，靠 description 语义降级；talk 的暴露面（「没听懂，讲清楚点」误触发）风险可接受。

### D-F-5. eval 期望修正（P4）

**决定**：docs evals.json eval-6 期望第 2 条从"没有机械直译的状态词堆叠（如『无效的参数』『未知错误』），也没有 bare『Success/Invalid』式标签"**保持不变**（该条已含 bare 标签表述，检查实际期望是否过严：只把"（如 invalid）"这种举例从期望中移除的不适用项澄清）——复核后实际需要修的是**期望措辞**：明确 `invalid configuration entries` 这类正常形容词用法不算违规，只有 **bare 状态标签单独成句**（如 `Invalid parameter: 400` 未展开）才算。

**理由**：P4 证据来自 iteration-1 findings（talk eval-6 缺陷③：`invalid configuration entries` 被误期望为违规，实际是正常形容词）。docs eval-6 的 prompt 恰好是 `Invalid parameter: 400`，是 **bare 标签**真违规场景——期望措辞保留硬校验，但需明确区分"正常形容词"与"bare 标签"。

## Risks / Trade-offs

- **[规范化情态误放行]** 规范型情态降级 warning 后，改写场景可能新增原稿没有的"必须"要求 → 缓解：DROPPED_MARKERS 只查删除方向；**新增**方向由 rubric 语义层"未新增事实"（docs rubric 13 / talk rubric 7）兜底，且 SKILL.md 明确"不得新增原稿没有的要求"。
- **[P3 护栏过度]** "不得复述标题"可能误伤合法 summary → 缓解：护栏限定在"空壳引导句+无信息条目"形态，合法归纳（有依据/条件的复述）不受限。
- **[期望过严→过松摆动]** eval-6 放宽后可能放过真 bare 标签 → 缓解：期望措辞写清"单独成句"边界，并保留 `Invalid parameter: 400` 为基准用例。

## Migration Plan

1. 本 change 交付：check_plain.py 词表拆分 + SKILL.md/rubric/spec 措辞 + evals.json 期望修正。
2. 验证：`check_plain.py` 回归（`必须`→0 violation 1 warning；`一定`→violation 语义不变）；openspec validate。
3. 评估复跑：docs eval-3（P3 护栏生效验证）+ docs eval-6（P4 期望修正验证），with_skill 单配置即可（护栏/期望改动不影响 baseline）。
4. archive + W4 单提交。
5. `docs/evals.md` 补记本轮 followup 说明。

## Open Questions

- 无阻塞性问题。`must` 在英文里的"规范"与"逻辑必然"（"this must be the case"）二义性留作已知边界：本 change 统一按规范型处理（warning），语义层 rubric 兜底判断。