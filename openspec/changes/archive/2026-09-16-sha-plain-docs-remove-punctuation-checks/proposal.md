## Why

承接上一轮删除引号规则（`sha-plain-docs-remove-quote-rule`）的同一决策逻辑：标点符号的严格处理对用户理解内容没有帮助，且会误伤——**半角逗号也可能是源码的一部分**（如 `foo(a, b)` 出现在内联代码或标识符中），脚本却把它当作中文正文的半角标点报违规。用户拍板：**不处理任何标点符号**。

上一轮只删了 `quote_style`（引号风格检查），本轮把剩余的全部标点检查也删掉，只保留对理解有实际帮助的中英文混排空格规则。

## What Changes

- 删除 `check_plain.py` `check_punctuation` 中的：
  - `halfwidth_punctuation`（半角标点 → 全角）检查块
  - `extra_space_before_punct`（数字与全角标点之间不加空格）检查块
- **保留** `missing_cjk_latin_space`（中文与英文/数字之间加空格）——这是排版可读性规则，不是标点处理，不影响源码。
- 清理不再使用的常量 `HALFWIDTH_PUNCT`、`FULLWIDTH_AFTER_DIGIT`。
- `references/rules-zh.md`（authoritative）：
  - 表格「标点一致」行改为只保留"中文与英文数字之间加空格"。
  - 「混排与标点细则」删除半角标点相关条目，保留中英空格与 `%` 规则。
- `docs/rules.md`（展示副本）同步「标点一致」行。
- 主 spec《目标语言选择》《确定性验证》同步：标点规范从检查范围移除，中英空格保留。
- **不触碰**：`sha-plain-talk`、check_facts、句长双层、删改对比、avoid-words、归档快照。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `sha-plain-docs`: 《目标语言选择》删除"全角标点"约束；《确定性验证》项 1 的检查范围从"标点与空格规范"改为"中英混排空格规范"，Scenario 违规清单分类相应更新。

## Impact

- `skills/sha-plain-docs/scripts/check_plain.py`（删两个检查块 + 两个常量）
- `skills/sha-plain-docs/references/rules-zh.md`（authoritative 规则源）
- `docs/rules.md`（展示副本）
- `openspec/specs/sha-plain-docs/spec.md`（主 spec 同步）
- 不涉及：talk skill、check_facts / 句长 / 删改对比逻辑、`avoid-words.md`。