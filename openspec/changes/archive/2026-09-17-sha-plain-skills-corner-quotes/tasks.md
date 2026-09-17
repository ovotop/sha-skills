## 1. check_plain.py 检查实现

- [x] 1.1 新增 `check_corner_quotes(lines, lang, findings)`：仅 zh 模式，逐字符扫描 `item["masked"]`（复用 collect_lines 跳过 + mask_line 屏蔽），命中「」『』任一报告 `corner_quotes_in_zh` violation，提示改用弯引号
- [x] 1.2 `run()` 中挂接新检查（zh 时调用）
- [x] 1.3 SOURCE_RE 的 `见\s*[「『\"']` 扩为支持 `见“`（弯引号来源标记）
- [x] 1.4 脚本内部诊断消息的「{label}」改为“{label}”（自洽，不参与检查）
- [x] 1.5 回归用例：含「引言」样本 → 1 violation/退出码 1；ASCII 直引号样本 → 0 violation；code span 内「」→ 跳过；`见“上文”）断言 → check_facts 不误报

## 2. 规则源与展示副本

- [x] 2.1 `rules-zh.md` 标点与格式表新增「引号规范」行：简体中文用弯引号（“ ”），不用直角引号（「」『』，日文/繁中风格）；「混排与标点细则」补一条
- [x] 2.2 `docs/rules.md`（展示副本）同步新增同一行

## 3. 语料清扫（仅规则与模型可见文件，豁免清单见 design D-4）

- [x] 3.1 `sha-plain-talk/SKILL.md`：description 与正文触发词「」→“”
- [x] 3.2 `sha-plain-docs/SKILL.md`、`README.md`：正文「」→“”并补充引号规则表述
- [x] 3.3 `trigger-queries.json`、`avoid-words.md`、`rules-en.md`：示例与原因文字「」→“”
- [x] 3.4 check_plain.py 消息（1.4 内已含）
- [x] 3.5 收尾 grep 全仓扫描：确认非豁免文件无「」『』残留

## 4. spec 应用与验证

- [x] 4.1 `openspec validate`：change 与主 spec 校验通过
- [x] 4.2 回归矩阵通过（1.5 + 既有检查不受影响：句长/禁词/check_facts/punctuation）

## 5. 归档与提交

- [x] 5.1 `openspec archive sha-plain-skills-corner-quotes`：主 spec 合并《目标语言选择》《确定性验证》《微观规则》变更
- [x] 5.2 W4 单次提交：change 目录 + 主 spec + check_plain.py + 规则源 + 语料清扫全部合一