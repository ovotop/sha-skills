## Context

现状：`check_plain.py` 的 `check_punctuation` 已不含任何引号检查（remove-quote-rule 删除 `quote_style`）；`rules-zh.md` 无引号条目；主 spec《目标语言选择》明言"引号风格不受约束"。但规则与模型可见语料（两 SKILL.md、README、spec、trigger-queries、脚本消息）普遍用「」标引用，模型输出随之沿用直角引号，简体中文正文呈日文感。动机与范围见 proposal.md。

约束：
- OpenCode/Claude Code 语义触发均只看 description；语料即是规则示范，清扫范围 = 规则与模型可见文件（用户拍板），历史记录/夹具/归档快照不动。
- `SOURCE_RE`（check_facts 来源识别）含 `见\s*[「『\"']` 分支——语料转向弯引号后该分支需同步支持 `见“`，否则"见「上文」"改写为"见“上文”"后来源识别会漏。

## Goals / Non-Goals

**Goals:**
- 机器可检出：zh 文档正文直角引号 → `corner_quotes_in_zh` violation，退出码 1。
- 规则与示范语料自洽：规则文件与模型可见文件内直角引号清零。
- 与 remove-quote-rule 的字节面兼容：ASCII 直引号维持豁免，不误伤英文原文/代码引用。

**Non-Goals:**
- 不改历史记录（docs/evals.md 旧段落）、eval 夹具、archive 快照。
- 不做引号自动纠偏/规范化（只检出+规则约束，不自动替换用户文档）。
- 不检英文文档（en 模式不启用该检查）。
- 不重新引入半角/全角标点检查（上一 change 已拍板删除）。

## Decisions

### D-1. 反向约束：只禁直角引号，ASCII 直引号豁免

**决定**：rule 语义为"简体中文正文不用直角引号「」『』"。ASCII 直引号（" '）不检查。理由：remove-quote-rule 删除的是"强制「」+ 禁 ASCII"的旧约束，误伤源头是 ASCII 检查；本次只新增直角引号反例，正交、无回归。备选"连 ASCII 一起禁"被否决——重蹈误伤覆辙。

### D-2. 独立检查函数而非并入 check_punctuation

**决定**：新增 `check_corner_quotes(lines, lang, findings)`，仅 `lang == "zh"` 时调用。理由：`check_punctuation` 语义是"中英混排空格"，引号反例是独立规则类别（rule 名 `corner_quotes_in_zh`），独立后报告聚合/过滤清晰。逐字符扫描 `item["masked"]`（已跳过 code span/URL），命中 `「」『』` 任一即报，snippet 取该字符。

### D-3. 跳过逻辑复用现有 collect_lines

**决定**：不新增跳过规则。frontmatter、```code、表格行、空行已由 `collect_lines` 置 `skip`；行内 code span/URL 由 `mask_line` 屏蔽——"文档正文"边界与既有检查完全一致。规则文件/README 等语料本身不是输入，脚本不会检查自身。

### D-4. 语料清扫清单（仅规则与模型可见文件）

**决定**：两 SKILL.md（含 description 触发词）、README、本 change 的 delta spec、`trigger-queries.json`、`avoid-words.md`、`rules-en.md`、`docs/rules.md`、`rules-zh.md`、`check_plain.py` 内部消息 →「」『』换弯引号。`「」←→“ ”`、`『』←→‘ ’`。**豁免**：`docs/evals.md` 历史段落、`skills/*/evals/evals.json` 与 rubric、`openspec/changes/archive/*`、`.git`。

### D-5. SOURCE_RE 兼容弯引号

**决定**：`见\s*[「『\"']` 扩为 `见\s*[「『“\"']`。理由：语料与输出转向“”后，`见“上文”）` 类来源标记仍需被识别为可核对来源，不因引号风格变化产生 check_facts 回归。

## Risks / Trade-offs

- **[清扫遗漏产生模型可见「」残留]** → 收尾用 grep 全仓扫描，对每个命中逐条判定"豁免 or 遗漏"；豁免清单在 W4 提交说明中列出。
- **[改写外部原稿含「」被报违规]** → 预期行为（改写即纠正）；无豁免通道需求，code span/表格内内容天然跳过。
- **[`check_facts` 对”引来源识别变化]** → D-5 覆盖；回归矩阵增加"见“…”来源"用例。
- **[消息文案与规则自洽性的循环]** → 脚本消息仅出现在诊断输出，非文档正文，不构成循环违规；统一改为弯引号仅为风格自洽。

## Migration Plan

1. `check_plain.py`：新增 `check_corner_quotes` + `run()` 挂接 + SOURCE_RE 兼容 + 内部消息弯引号。
2. `rules-zh.md` 标点与格式表新增「引号规范」行 + 混排与标点细则补一条；`docs/rules.md` 同步。
3. 语料清扫（D-4 清单）。
4. 验证：`openspec validate`；`check_plain.py` 回归矩阵（见 tasks.md）。
5. `openspec archive sha-plain-skills-corner-quotes` → W4 单次提交（change 目录 + 主 spec + 代码/规则/语料）。

## Open Questions

无。