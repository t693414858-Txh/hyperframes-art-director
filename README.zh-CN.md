# HyperFrames Art Director

这是一个独立的 Codex Skill，用来给 HyperFrames 视频增加“视觉导演层”：它不替代官方 HyperFrames 技能，而是在写 HTML、CSS、GSAP 之前，先判断视频应该采用什么视觉路线、如何建立项目识别、每一幕应该证明什么，以及最终成片是否真的好看、连贯、有用。

## 0.10.0：把实际剪辑反馈写入规则

制作前先判断视频形态，再选择审核条件：

| 视频形态 | 主体素材 | 审核重点 |
| --- | --- | --- |
| 操作教程 | 实际工作区录屏 | 输入、操作、结果、验证及适用的时间门槛 |
| 案例分析 | 相关人物、工作过程、交付场景，穿插来源证据 | 事实归属、镜头用途、素材重复和叙事节奏 |
| 作品展示 | 已确认作品、细节和对比 | 原作完整、比例准确、结果看得清 |
| 故事影片 | 人物行动、物件变化和后果 | 承诺的动作是否实际发生 |

案例视频优先让相关的人、动作和环境承担画面，资料表格在需要证明论点时出现。镜头清单记录源文件、取段起止、工作环节、动作、环境和景别。换裁切不算新素材；刻意回扣可以保留，但要说明用途。

用户认可运镜后，继续修改重复和节奏时保留已认可方向。每次改版重新绑定成片、抽帧和评分；配音变速后重建字幕和镜头时间，并检查实际导出文件的首尾帧、字体和声音。

详细规则见[制作形态](skills/art-direct-hyperframes/references/production-format.md)、[素材与剪辑](skills/art-direct-hyperframes/references/footage-editing.md)和[最终交付审核](skills/art-direct-hyperframes/references/final-delivery-review.md)。[账号偏好示例](examples/account-style-profile.md)需按项目选用。已有教程时间门槛来自账号实践，效果仍需用可比的发布数据验证。

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

### 4. 短视频留存门槛

`shortform-retention-plan.json` 把账号诊断结论转成适用于竖屏操作教程、工作流演示、实测和教程引流视频的制作条件。案例分析、作品展示和故事先按各自形态审核，不填虚构操作来满足该表。

它会检查：

- `0.8s` 前是否出现问题和可识别的结果预览；
- `2.5s` 前是否开始真实操作；
- `5s` 前是否出现第一次可见证据；
- `8s` 前是否完成前后对比或结果验证；
- 前 `12s` 是否至少每 `2.5s` 出现一次有意义的状态变化；
- 是否用连续操作承载证据，而不是用海报卡片或张贴截图替代演示；
- 单任务是否控制在 `35s` 内，多步骤工作流是否控制在 `50s` 内，超时是否有有效豁免。

发布后的 2 秒跳出率、5 秒完播率、平均播放比例、收藏率和关注转化率作为复盘目标使用，不伪装成发布前可以预测的结果。

### 5. 体验和互动门槛

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

### 6. 成片审核门槛

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
5. 对适用的竖屏短视频生成并验证 `shortform-retention-plan.json`。
6. 交给官方 HyperFrames 实现 HTML、CSS、GSAP、转场和渲染。
7. 生成关键帧、联系表和 `review-evidence.json`。
8. 对适用的教学内容生成并验证 `experience-interaction-qa.json`；其他形态按对应规则审片。
9. 生成并验证 `review-scorecard.json`。

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
python3 skills/art-direct-hyperframes/scripts/validate_shortform_retention.py \
  examples/shortform-retention.pass.json
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
