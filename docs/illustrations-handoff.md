# README 插图 handoff

README.md 已交付但不含插图。当前环境无 `image_gen` 工具。ian-xiaohei-illustrations 的生图流程因此无法执行。用户于 2026-09-17 拍板先交付无插图版。本文件描述后续在有 `image_gen` 的环境中如何补图并插入 README。

## 要做什么

用 ian-xiaohei-illustrations skill 生成 3 张手绘插图。图片存入 `assets/readme-illustrations/`（空目录已建，未被 gitignore）。最后把图片引用插入 README.md。

## 配图 shot list

### 图 1：从困惑到清晰

- 插入位置：README 序言段落之后、`## 两个技能管两类表达问题` 标题之前
- 核心意思：AI 原始输出是一团乱，技能重讲后变成整齐可用的内容
- 结构类型：前后对比
- 小黑动作建议：左侧小黑面对一团缠绕的线（黑话与长句的隐喻）；右侧小黑把线捋成整齐的一束
- 文件名：`assets/readme-illustrations/01-confusion-to-clarity.png`

### 图 2：两个技能分工

- 插入位置：`## 两个技能管两类表达问题` 小节末尾（talk/docs 两段说明之后）
- 核心意思：talk 管对话重讲，docs 管文档写作加脚本验证
- 结构类型：分流并列
- 小黑动作建议：一个小黑在对话气泡旁改写纸条；一个小黑在文档旁对着齿轮跑脚本
- 文件名：`assets/readme-illustrations/02-two-paths.png`

### 图 3：机器验证（可选）

- 插入位置：`## 脚本验证代替肉眼检查` 段落之后
- 核心意思：脚本把关代替肉眼检查
- 结构类型：单场景
- 小黑动作建议：小黑拿放大镜看纸条，脚本在旁边盖章
- 文件名：`assets/readme-illustrations/03-machine-verification.png`
- 优先级：可选；图 1、图 2 稳了再做

## 生成约束（来自 ian-xiaohei-illustrations skill）

- 16:9 横版，纯白背景，黑色手绘线稿
- 少量红/橙/蓝中文手写批注，大量留白
- 小黑是核心动作主体，不能只当装饰
- 禁止 PPT 感、商业插画、幼稚可爱、左上角类型标题
- 每张单独立生成，不拼图；不要复刻过往案例构图，从本文重新发明隐喻
- 生成后过 `references/qa-checklist.md`

## 插入 README 的步骤

1. 在各插入位置加一行：`![中文简短描述](assets/readme-illustrations/0X-name.png)`
2. 跑验证：`python3 skills/sha-plain-docs/scripts/check_plain.py README.md --lang zh --greenfield`，改到 0 violations
3. commit 时图片与 README 引用一并入库

## 验收清单

- [ ] 3 张（或至少图 1、图 2）PNG 生成并存入 `assets/readme-illustrations/`
- [ ] 图片引用插入 README，alt 文案为中文简短描述
- [ ] check_plain.py 对 README 报 0 violations
- [ ] commit 包含图片与 README 引用

## 涉及的文件

- `README.md`：待插入引用
- `assets/readme-illustrations/`：图片目标位置（当前为空）
- `skills/sha-plain-docs/scripts/check_plain.py`：验证工具
- ian-xiaohei-illustrations skill：已部署在 `.claude/skills/` 与 `.opencode/skills/`。链接指向仓库外的 `documenting/ian-xiaohei-illustrations`。