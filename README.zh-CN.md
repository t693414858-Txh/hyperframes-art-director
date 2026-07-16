# HyperFrames Art Director

这是一个独立的 Codex Skill，用来给 HyperFrames 视频增加“视觉导演层”：它不替代官方 HyperFrames 技能，而是在写 HTML、CSS、GSAP 之前，先判断视频应该采用什么视觉路线、如何建立项目识别、每一幕应该证明什么，以及最终成片是否真的好看、连贯、有用。

## 它解决什么问题

很多 HyperFrames 视频技术上能通过，但审美和表达仍然会出问题：

- 看起来像模板；
- 截图像贴在背景上的图片；
- 科技类内容默认深色渐变，缺少内容依据；
- 项目识别只靠标题、数字人、字幕或颜色；
- 视觉路线和文稿内容不匹配；
- CTA 只在最后出现，关键词和奖励前后不一致；
- 工具更新视频只说功能，没有证明用户体验有什么变化。

这个 Skill 把这些主观判断变成可记录、可检查、可复用的方向合同和审核门槛。

## 核心能力

### 1. 内容自适应风格选择

不是看到“科技”就套苹果风，也不是看到“文化”就套报纸风。Skill 会先诊断：

- 内容类型；
- 传播目的；
- 目标观众；
- 情绪温度；
- 证据要求；
- 可用素材；
- 品牌和文化敏感性。

然后在以下路线中选择主路线和必要的辅助路线：

- Precision Product
- Knowledge Explainer
- Editorial Documentary
- Evidence-Led Intelligence
- Scientific Clarity
- Civic Trust
- Human Warmth
- Craft and Heritage
- Kinetic Culture
- Brand Manifesto

### 2. 项目指纹

“浅色极简”“深色科技”“卡片布局”“数字人右下角”都不是项目识别。真正的项目识别必须在去掉标题、Logo、字幕和数字人之后仍然能被认出来。

Skill 会要求每个完整方向定义：

- 独特的语义变化；
- 真实来源证据；
- 反复出现并演化的结构锚点；
- 每一幕如何承载项目识别；
- 盲识别测试；
- 模板替换测试；
- 多幕视频至少 60% 是核心识别场景。

### 3. 内容节奏门槛

`content-rhythm.json` 用来在配音之前检查文稿是否真的有信息密度。

它会检查：

- 体验变化覆盖率；
- 互动覆盖率；
- 体验和互动合并后的有效覆盖率；
- 开头、中段、结尾互动是否按时出现；
- 最大空白信息段是否过长；
- 长场景是否包含足够的信息单元。

这可以防止“画面很大、很漂亮，但信息为空”的长段落进入制作阶段。

### 4. 体验和互动门槛

`experience-interaction-qa.json` 用来检查教程、工具更新、测评、工作流讲解和引流视频是否真的给用户一个明确收益。

它会检查：

- 之前和之后的具体体验差异；
- 最适合使用这个功能的任务形态；
- 输入、操作、结果是否清晰；
- 是否说明边界或限制；
- 是否有可见证据；
- 60% 时长之前是否出现低摩擦互动；
- 最终是否只有一个主 CTA；
- 回复格式是否明确；
- 奖励是否具体；
- 口播、字幕、画面 CTA、发布文案、置顶评论是否一致。

### 5. 成片审核门槛

成片审核从 8 个维度打分：

1. 内容和风格匹配度
2. 项目识别
3. 叙事清晰度
4. 构图和焦点
5. 字体系统
6. 图像和材料处理
7. 动效和节奏
8. 连贯性和独特性

通过条件包括：

- 平均分至少 4.0；
- 项目识别至少 4；
- 没有任何维度低于 3；
- 没有阻塞问题；
- 每个低于 4 的分数都必须给出具体修正动作。

## 安装

把可安装 Skill 目录复制到 Codex skills 目录：

```bash
cp -R skills/art-direct-hyperframes "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果 Codex 没有立刻发现它，重启或刷新 Codex。

## 使用方式

```text
Use $art-direct-hyperframes to define the visual direction, storyboard,
hero frames, rhythm, project fingerprint, and review gates for this script.
Then use $hyperframes to implement the composition and $hyperframes-cli to
validate, preview, and render it.
```

审核已有成片时：

```text
Use $art-direct-hyperframes to review this HyperFrames result. Diagnose why it
feels generic or incoherent, update DESIGN.md if needed, and produce concrete
corrections before another render.
```

## 推荐工作流

1. 诊断文稿和素材。
2. 生成 `asset-readiness.json` 并验证素材可用性。
3. 生成 `DESIGN.md` 和 `direction-brief.json`。
4. 对教程/测评/工作流视频生成 `content-rhythm.json`。
5. 交给官方 HyperFrames 实现 HTML、CSS、GSAP、转场和渲染。
6. 生成关键帧、联系表和 `review-evidence.json`。
7. 生成并验证 `experience-interaction-qa.json`。
8. 生成并验证 `review-scorecard.json`。

## 验证命令

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/art-direct-hyperframes/scripts/validate_asset_readiness.py \
  examples/asset-readiness.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_direction.py \
  examples/direction-brief.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_content_rhythm.py \
  examples/content-rhythm.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_experience_interaction.py \
  examples/experience-interaction-qa.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_review.py \
  examples/review-scorecard.pass.json
python3 skills/art-direct-hyperframes/scripts/prepare_visual_review.py \
  examples/review-capture-plan.pass.json --validate-only
```

## 适合什么项目

- AI 工具教程；
- 产品功能更新；
- 工作流讲解；
- 数据或证据驱动的视频；
- 需要连续多期账号风格但每期内容不能重复的短视频；
- 已经能渲染但审美、叙事、项目识别不够好的 HyperFrames 视频。

## 不做什么

- 不替代官方 HyperFrames；
- 不自己渲染视频；
- 不自动授权第三方图片、字体、UI、影像素材；
- 不复制 Apple、The New York Times 等品牌的受保护识别；
- 不把 lint 通过等同于审美通过。

## License

MIT. See [LICENSE](LICENSE).
