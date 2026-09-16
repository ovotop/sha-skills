## 1. 脚本改造

- [x] 1.1 `check_plain.py`：删除 `check_punctuation` 中 `lang == "zh"` 的 `quote_style` 检查块（`re.finditer(r"\"|''", masked)` 整段）
- [x] 1.2 确认 `masked` 变量仍被后续 halfwidth_punctuation / missing_cjk_latin_space 使用，无孤立变量残留

## 2. 规则源与展示副本

- [x] 2.1 `references/rules-zh.md` 表格「标点一致」行：删除"中文引号统一用「」"表述，保留全角标点与中英文空格
- [x] 2.2 `references/rules-zh.md`「混排与标点细则」：删除"中文引号统一用「」；中文正文不使用 " " 或 " "。"整行
- [x] 2.3 `docs/rules.md`（展示副本）「标点一致」行：同步删除引号表述

## 3. spec 同步与验证

- [x] 3.1 主 spec `openspec/specs/sha-plain-docs/spec.md`：《目标语言选择》删除"引号统一「」"并保留其余标点约束
- [x] 3.2 验证：`openspec validate --specs` 通过
- [x] 3.3 验证：`check_plain.py` 回归——含 ASCII 引号的样本期望 0 violation（quote_style 不再报），其余检查（句长/禁词/来源/半角标点/空格）行为不变

## 4. 归档与提交

- [x] 4.1 `openspec archive` 归档 change
- [x] 4.2 W4 单提交：change 目录 + 主 spec + 代码/rules 改动合并为一次 commit
- [x] 4.3 `git stash pop` 恢复被暂存的 ref_def_re 补丁（不属于本 change，交还工作区）