# 啥-skills 仓库工作约定

本仓库维护 sha-plain-talk 和 sha-plain-docs 两个技能。它们都是中文表达技能。技能源码在 `skills/`，变更记录在 `openspec/`。AI agent 在此仓库做修改前，先读完本文件再动手。

技能行为的每次改动都要可追溯。先在 `openspec/` 立 change，再实现，最后归档。这样规则为什么改、改了什么，以后还能查到。

## 改技能内容前必须先立 openspec change

改动 `skills/` 下的规则、脚本、评估或触发描述，一律先走 openspec 流程。不要直接改完就提交。例外只有两类：`docs/rules.md` 展示副本同步、明显笔误修复。例外改动要在 commit message 里写清理由。

openspec 流程分四步，每步加载对应 skill 执行：

1. **立变更**：加载 `openspec-propose`，生成 change 目录（`proposal.md`、`tasks.md`、`specs/` 增量）。change 名用 kebab-case，写清改什么、为什么改。
2. **实现**：加载 `openspec-apply-change`，按 `tasks.md` 逐项实现。实现中发现 spec 要细化，先改 change 里的 spec，再改代码。
3. **验证**：按本文件“收尾前跑完这份验证清单”一节执行。
4. **归档**：加载 `openspec-archive-change`，把 change 移入 `openspec/changes/archive/<日期>-<名>/`，同步主 spec 到 `openspec/specs/`。

历史 change 的完整结构见 `openspec/changes/archive/`，照着最近一次的样式写。

## 技能源码只放 skills/，部署靠符号链接

每个技能的唯一源码只存在于 `skills/<技能名>/`，必须入 git。工具的发现目录里只放相对符号链接，不放拷贝。源码放进 gitignore 目录会丢 diff 历史。重装环境还会漂移。这两个问题是本约定要防的。

- `.claude/skills/<技能名>` → `../../skills/<技能名>`：Claude Code 和 OpenCode 都读这个位置。这个链接要入库。
- `.opencode/skills/`：整个目录被 gitignore。OpenSpec 插件在此生成 `openspec-*` 命令。本地调试用的技能链接也可以放这里，但它不是耐久部署位置。其他人克隆仓库后拿不到它。
- 新增技能：把源码放进 `skills/`，在 `.claude/skills/` 建相对链接，再跑 `git ls-files skills/` 确认源码已跟踪。
- 移动或重命名技能后：全库搜旧路径引用。命令：`grep -rn "opencode/skills" skills/`。把 SKILL.md 里的硬编码路径改掉。

## 新增和修改技能按 open-skill-creator 规范执行

写技能、改技能、跑评估，加载 `open-skill-creator` skill，按它的完整流程走。本节只列本仓库要遵守的要点。

**description 同时写清做什么和何时触发**。触发词用用户会说的原话。触发面宁可写宽，也不要漏触发。漏触发的技能等于不存在。

**结构按渐进披露分层**：

```text
skills/<技能名>/
├── SKILL.md          # 技能正文，理想情况 < 500 行
├── scripts/          # 可执行脚本；确定性任务优先写脚本，不靠模型即兴发挥
├── references/       # 按需读取的规则文档
└── evals/            # 评估用例定义（evals.json）
```

**评估用双配置对照**。改触发描述或行为后，跑 `with-skill` 与 `baseline` 对照。评估流程按 `open-skill-creator` 执行。工作区产出落在 `<技能名>-workspace/`，这个目录已被 gitignore，不提交。评估结论摘要写进 `docs/evals.md`。

**已有技能不改名**。目录名和 frontmatter 的 `name` 字段保持原样。改名会让已安装的用户断链。

## 中文规则只改 rules-zh.md

`skills/sha-plain-docs/references/rules-zh.md` 是中文受控写作规则的唯一权威源。`docs/rules.md` 是展示副本，允许滞后。改规则的顺序固定：

1. 改 `references/rules-zh.md`。
2. 跑 `check_plain.py`，确认脚本与新规则一致。
3. 需要时再同步展示副本；不同步不算违规。

## 收尾前跑完这份验证清单

改完代码不等于改完。按改动类型执行对应检查：

- **动了技能正文或脚本**：跑 `python3 skills/sha-plain-docs/scripts/check_plain.py <改动的文档> --lang zh`。退出码必须为 0。`normative_modality` 类告警是规范情态的预期提示，不算违规。
- **动了规则或评估定义**：跑一轮评估。评估流程按 `open-skill-creator` 执行，结果记进 `docs/evals.md`。
- **动了目录布局或新增技能**：`ls -la .claude/skills/` 确认链接指向 `../../skills/...`。`test -f .claude/skills/<技能名>/SKILL.md` 确认链接可解析。`git ls-files skills/` 确认源码已跟踪。
- **所有改动**：确认工作区没有混入其他 change 的文件。归档的 `openspec/` 变更与代码、测试在同一个提交单元里。

禁止执行 git push。commit、rebase、merge 可以做，推送留给用户手动完成。
