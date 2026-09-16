# Tasks: sha-plain-skills-followup

## 1. check_plain.py 词表拆分（D-F-1）

- [x] 1.1 STRONG_ZH/STRONG_EN 拆为事实型（facts）与规范型（normative）两组词表
- [x] 1.2 check_facts 对 normative 命中发 `normative_modality` 类别，默认 warning（绿场与改写一致，不需要来源标记），不计数 violation
- [x] 1.3 回归验证：`用户必须配置超时时间。` → 0 violation + 1 warning；`系统一定失败。`（无来源）→ 仍 violation；en `must` 同理

## 2. spec / SKILL.md / rubric 措辞同步（D-F-1/D-F-3）

- [x] 2.1 docs spec《确定性验证》第 2 条：拆出 normative_modality 类别（必须/不得/禁止/must 默认告警，不需要来源标记；事实型词表保持硬查）
- [x] 2.2 docs spec《金字塔结构》护栏④：空壳引导句（"如下/以下"式）禁用 + 标题已给判断时不复述标题（D-F-2）
- [x] 2.3 talk spec《输出前自检》：自检②措辞区分事实断言 vs 规范要求
- [x] 2.4 docs SKILL.md：置信阶梯新增规范要求行；结构护栏④扩展；工作流第 5 步措辞小调（规范句不需来源）
- [x] 2.5 talk SKILL.md：自检②措辞区分（必须/不得 类规范要求不需来源，但不得新增原稿没有的要求）
- [x] 2.6 两个 rubric 核心三问第 3 条同步规范要求边界

## 3. eval 期望修正（D-F-5）

- [x] 3.1 docs evals.json eval-6：期望措辞明确 bare 状态标签单独成句才算违规，正常形容词（invalid configuration entries）不算

## 4. 验证

- [x] 4.1 `check_plain.py` 回归矩阵（必须/一定/不得/从不/must/always）全部符合预期
- [x] 4.2 `openspec validate --specs` + `openspec validate <change>` 通过
- [x] 4.3 `scripts/check_rules_drift.py` 通过（本 change 不动 docs/rules.md 复制区）

## 5. 评估复跑（仅受影响用例，偏离记录到 docs/evals.md）

- [x] 5.1 docs eval-3 复跑（with_skill）：验证 P3 空壳引导句护栏生效，0 violation
- [x] 5.2 docs eval-6 复跑（with_skill）：验证 P4 期望修正后的判定，0 violation
- [x] 5.3 `docs/evals.md` 补记本轮 followup 说明（P1/P2/P3/P4 处置与复跑结果）

## 6. 收尾

- [x] 6.1 在 `docs/evals.md` 补记 followup 说明与 P2 决定（用户 2026-09-16 拍板：talk 沿用 wait-what 模式，不做 ClaudeCode/OpenCode 特殊处理；归档 change 为历史快照不改动）（D-F-4）
- [x] 6.2 openspec archive + W4 单提交（change 目录 + 主 spec + 代码/文档同一次提交）