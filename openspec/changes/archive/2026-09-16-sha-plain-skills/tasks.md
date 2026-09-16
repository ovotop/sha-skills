# Tasks: sha-plain-skills

## 1. 仓库基建

- [x] 1.1 创建 `.gitignore`，忽略 `conversations/` 与会话插件生成物（`.opencode/`、`.sisyphus/`、Python 缓存）；确认 `skills/` 与 `.claude/skills/` **不**被忽略（D7 布局修订：符号链接随 git 追踪）
- [x] 1.2 首次 git 提交（当前仓库零提交），仅包含 openspec 规划产物

## 2. 平台 smoke test（B2/D5：不把平台假设当已定事实）

- [x] 2.1 实测 `disable-model-invocation: true` 语义 → **Claude Code 支持（用户专属）**；**OpenCode 不支持**（只读 name/description，未知键静默忽略），见 design D3 实测结论
- [x] 2.2 实测 slash command 注册 → **OpenCode 自动把每个 skill 注册为 `/skill-name`**（`source:"skill"`），且扫描 `.claude/skills/**`；Claude Code 用目录名做命令名。用户显式调用路径成立
- [x] 2.3 实测 `scripts/check_plain.py` 从 skill 相对路径执行的方式与 `--json` 退出码约定
- [x] 2.4 平台回退已落地：**模仿 mattpocock/wait-what 的 user-invoked 模式**（保留 `disable-model-invocation: true` + description 剥离触发词改为人面向一句话；不在 OpenCode 引入无收益 sidecar）。依据与代价记录在 design D3

## 3. sha-plain-talk skill

- [x] 3.1 创建 `skills/sha-plain-talk/SKILL.md`：frontmatter（name / description<60 词 / disable-model-invocation: true）；并建相对符号链接 `.claude/skills/sha-plain-talk -> ../../skills/sha-plain-talk`（D7 布局修订）
- [x] 3.2 撰写正文工作流（显式调用 → 定位最近未讲清消息 → 结论先行 → ≤3 点 → 细节后置），强调自然语言不自动路由，体积 ≤ ~40 行
- [x] 3.3 内联内核表（通用/zh/en 适用域标注，含 en 护栏、显式主语+主动语态、避免模糊副词）
- [x] 3.4 内联 5 项输出前自检清单（结论在首句 / 无来源强断言已加来源或降级或删除 / 无黑话 / 指代可定位 / 单句≤40字，en 用短句护栏）
- [x] 3.5 内联置信阶梯 + 来源标记语法（D9：有来源→强语态+来源入句；无来源推测→弱语态；不可判→删除；标记示例（你上一条消息）/（上文已确认）等）
- [x] 3.6 内联黑话 top-15 清单（avoid-words.md 的子集）与输出格式模板（直接输出，无元注释）
- [x] 3.7 撰写 when-not-to 段（新问题/新请求/自然语言不清不激活）

## 4. sha-plain-docs skill

- [x] 4.1 创建 `skills/sha-plain-docs/SKILL.md`：frontmatter（description<60 词，含 When 从句/触发词/负触发/文本类型枚举）——模型可自动触发；并建相对符号链接 `.claude/skills/sha-plain-docs -> ../../skills/sha-plain-docs`（D7 布局修订）
- [x] 4.2 撰写正文工作流：第一步显式判文档类型→选适用强度（拿不准问用户）→ 目标语言选择 → 结构护栏 → 微观规则+置信阶梯（D9）→ `check_plain.py` 验证；工作流 SHALL 区分**绿场写作**（无原稿 → check_facts 告警级）与**改写**（有原稿/对话来源 → check_facts 硬查 + 可选 --source 删改对比）（Oracle B2）；含"写中文文档前 MUST 读 references/rules-zh.md"的显式指令（S3），体积 ≤ ~100 行
- [x] 4.3 内联内核表（适用域标注）+ 4 条结构护栏（序言=提示已知 | 标题=判断句非标签 | 归纳优先不混用 | 空壳句禁用）
- [x] 4.4 撰写操作/排查文档模板段（前置条件→风险→编号步骤→预期结果→失败条件与恢复）
- [x] 4.5 在 workflow 中说明何时调用 references/rules-en.md（英文长文档场景）

## 5. references 规则目录（sha-plain-docs）

- [x] 5.1 创建 `skills/sha-plain-docs/references/rules-zh.md`：复制 `docs/rules.md` 全表 + frontmatter 标注 `Source: docs/rules.md` + 新增内容隔离到"## 本 skill 新增"节（混排标点细则、SCQA 变体→文档类型映射 3-4 行）
- [x] 5.2 创建 `skills/sha-plain-docs/references/rules-en.md`：精简 STE 方向性规则（短句/主动/一词一义/情态护栏），只带结构护栏不搬词典；标注 D8 升级阈值（英文长文档任务占比 >30% 时扩充）
- [x] 5.3 创建 `skills/sha-plain-docs/references/avoid-words.md`：完整黑话清单（行格式便于脚本读取，含机械直译对照），与 talk 内联 top-15 标注母子关系

## 6. check_plain.py lint 脚本

- [x] 6.1 创建 `skills/sha-plain-docs/scripts/check_plain.py`（标准库 Python），参数：输入文件/文本 + `--lang zh|en` + `--source <原稿>`（可选，仅删改对比用）
- [x] 6.2 实现句长双层检查（S5）：句子级（无逗号 ≤40 字、30-39 字"需确认语义"）+ 逗号子句级（构件 ≤20 字）；违规输出清单不硬失败
- [x] 6.3 实现黑话/禁词检索（读取 avoid-words.md 行格式）
- [x] 6.4 实现强断言来源标记检查（check_facts，D5/D9）：扫描强确定性词（一定/必须/绝对/必定/必然/肯定/显然/无疑/确实/确定/从不/总是/永远），检查所在句或紧邻前句是否含来源成分（根据/依据/据/来自/显示/表明/报告/文档/监控/日志+实体，或（）标注）；"确认"不得单独作标记；无需 --source
- [x] 6.5 实现删改对比（--source 可选）：检测显式警告标记词（仅/不得/除非）在原稿→输出的缺失；无 --source 时明确提示跳过，不伪称已检测
- [x] 6.6 实现标点/空格规范检查（「」、全角标点、中英文间空格）；`--json` 输出 + 退出码约定（0=通过/1=有违规/2=用法错误）；check_facts 提供 `--greenfield` 开关：改写场景硬查、绿场写作降级告警

## 7. 评估与迭代（skill-creator 流程，S7 修订）

- [x] 7.1 为 talk/docs 各写 ≥5 个 evals 用例（每 skill 至少含针对"事实来源/置信阶梯、黑话、结论先行"三个最弱项的定向用例），保存 `evals/evals.json`
- [x] 7.2 创建 `<skill>-workspace/`，with-skill 与 baseline 对跑（12 例 × 2 配置 = 24 运行；iteration-2/3 只复跑受影响用例并复用 baseline，偏离已记录在 docs/evals.md）
- [x] 7.3 断言已落地：机械项＝`check_plain.py` 直跑（写入 grading-mechanical.json）；语义项＝`skills/<name>/evals/rubric.md`（核心三问 + 14 项）由 LLM-judge 逐项判 PASS/FAIL 并附证据
- [x] 7.4 已验证：docs 各用例 transcript 均显示读取 `references/rules-zh.md`（并有脚本闭环证明其影响输出：0 vs 18/22/91 违规），保留该 references
- [x] 7.5 已用官方 `aggregate_benchmark.py` 汇总 benchmark.json/md；**未跑 eval-viewer**（无浏览器，用户确认精简收尾），结果以 benchmark + `docs/evals.md` 呈现；迭代已完成两轮（见 7.2）
- [x] 7.6 已做触发评估（**批量判断替代 `run_loop.py`**，因环境无 `claude` CLI）：docs eval 集 20 条 → 20/20；talk 反向集 10 条 → 9/10（唯一误触发「没听懂，讲清楚点」，OpenCode 无机制强制，已记录）；description 词数：talk 32 字、docs 83 字

## 8. 漂移守卫（S6）

- [x] 8.1 创建 drift-check 脚本或 CI 步骤：diff `docs/rules.md` 与 `skills/sha-plain-docs/references/rules-zh.md` 的复制区，报告分叉
- [x] 8.2 将 drift-check 纳入 skill-creator 迭代门禁：docs/rules.md 变更时必须同步 references/rules-zh.md

## 9. 收尾

- [x] 9.1 提交全部 skill 产物（`skills/` + `.claude/skills/` 符号链接）+ 评估工作区说明（不含 conversations/ 与临时文件）
- [x] 9.2 按 OpenSpec W1-W4 流程归档 change（验证通过后 `openspec archive`，归档产物 + specs + 代码同一次提交）
- [x] 9.3 全局安装（用户 2026-09-15 追加要求）：在 `~/.claude/skills/` 与 `~/.config/opencode/skills/` 建绝对符号链接指向本仓库 `skills/sha-plain-talk`、`skills/sha-plain-docs`，使两 skill 跨仓库可用（与 mi-skills-* / skill-linker 既有全局链接方式一致）