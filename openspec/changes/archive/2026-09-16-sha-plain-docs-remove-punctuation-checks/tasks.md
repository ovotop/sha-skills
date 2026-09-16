## 1. 脚本改造

- [ ] 1.1 `check_plain.py`：删除 `check_punctuation` 中 `halfwidth_punctuation` 检查块（`if ch in HALFWIDTH_PUNCT:` 整段）
- [ ] 1.2 `check_plain.py`：删除 `check_punctuation` 中 `extra_space_before_punct` 检查块（`re.finditer(r"\d\s+[" + FULLWIDTH_AFTER_DIGIT + r"]", masked)` 整段）
- [ ] 1.3 `check_plain.py`：删除仅被上述两块使用的常量 `HALFWIDTH_PUNCT`、`FULLWIDTH_AFTER_DIGIT`
- [ ] 1.4 确认 `masked` 变量仍被 `missing_cjk_latin_space` 使用，无孤立变量残留

## 2. 规则源与展示副本

- [ ] 2.1 `references/rules-zh.md` 表格「标点一致」行：删除"全角标点"，只保留"中文与英文数字之间加空格"
- [ ] 2.2 `references/rules-zh.md`「混排与标点细则」：删除"正文用全角标点…"条目与"数字与全角标点之间不加空格"条目；保留中英空格与 `%` 规则
- [ ] 2.3 `docs/rules.md`（展示副本）「标点一致」行：同步删除"全角标点"

## 3. spec 同步与验证

- [x] 3.1 主 spec《目标语言选择》：删除"全角标点"，标注"标点风格不受约束"；场景「中文文档」THEN 由"标点规范"改为"中英混排空格规范"
- [x] 3.2 主 spec《确定性验证》：项 1 由"标点与空格规范"改为"中英混排空格规范"并加"标点不属于检查范围"；场景「脚本校验」违规清单分类同步改
- [x] 3.3 验证：`openspec validate --specs` 通过
- [x] 3.4 验证：`check_plain.py` 回归——`foo(a, b)`、`192.168.0.1`、`配置 maxConnections 为 200。` 期望 0 violation（无 halfwidth/extra_space）；缺空格样本（`中文ABC`）仍报 `missing_cjk_latin_space`；黑话/句长行为不变

## 4. 归档与提交

- [x] 4.1 `openspec archive` 归档 change
- [x] 4.2 W4 单提交：change 目录 + 主 spec + 代码/rules 改动合并为一次 commit