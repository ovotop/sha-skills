# Tasks: clause-too-long-warning

## 1. check_plain.py：clause_too_long 降级与 message 改写

- [x] 1.1 修改 `skills/sha-plain-docs/scripts/check_plain.py` L190：severity 从 `"violation"` 改为 `"warning"`
- [x] 1.2 同步修改 L190 的 message 文案为：`逗号构件 N 字（目标 ≤20）。优先改句式：拆句 / 去掉不必要逗号 / 缩短修饰。禁止为过检删除关键宾语、条件或否定。`（N 用 `char_len(clause)` 实际值）

## 2. SKILL.md：工作流与内核表同步

- [x] 2.1 在 `skills/sha-plain-docs/SKILL.md` 工作流第 5 步（跑脚本段落末尾）追加约束：构件超长（`clause_too_long` warning）时先改句式（拆句/去不必要逗号/缩修饰），删事实属于违规不是解法；30–39 字 info 确认语义完整后可保留，不必为消 info 把句子拆碎
- [x] 2.2 修改内核表句长条目（约 L49）：`句长[zh]：无逗号单句 ≤40 字（超 40 违规；30–39 字需语义明确），逗号分隔构件 ≤20 字（warning，先改句式勿删事实）`

## 3. 自测验收

- [x] 3.1 跑有逗号+长宾语用例，确认输出 warning 且 exit 0：`python3 skills/sha-plain-docs/scripts/check_plain.py --text '- 新业务接入时，在平台两个环境变量里各加一条 jobCode 映射即可' --lang zh`
- [x] 3.2 跑无逗号+完整宾语用例，确认仍 0 violation（30–39 字 info 可接受）：`python3 skills/sha-plain-docs/scripts/check_plain.py --text '- 新业务接入时在平台两个环境变量里各加一条 jobCode 映射' --lang zh`
- [x] 3.3 跑一条既有文档（如 README.md 或 docs/ 下任一文件）做回归，确认没有意外把历史 0-violation 文档打红

## 4. Oracle review follow-up（approve-with-notes 的 findings 1+2）

- [x] 4.1 `check_plain.py` L183 `sentence_too_long` message 从「请拆分」改为含反删信息指引：`单句 N 字，超过 40 字上限。优先改句式：拆句 / 缩短修饰。禁止为过检删除关键宾语、条件或否定。`
- [x] 4.2 delta spec 补「保留事实与置信阶梯」需求及「不删事实过检」scenario——句长告警/违规的正确解法是改写句式，删宾语/条件/否定属违规
