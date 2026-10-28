# 英文配图中文化 Skill

一个面向 Codex 的图片本地化 Skill：把文章插图、流程图、截图和社交媒体配图中的英文替换为简体中文，同时尽量保留原图的布局、层级、配色和视觉风格。

## 特点

- 先建立完整的英文到中文映射，再编辑图片
- 保留产品名、品牌名、代码标识、分支名和发布通道名
- 面向 AI 与开发者内容时，优先保留 `PR`、`Agent`、`main` 等常用英文术语
- 检查漏译、错字、乱码以及不应被翻译的术语
- 用脚本检查输出尺寸，并按原图像素尺寸生成归一化文件
- 默认不覆盖原图

## 安装

将仓库克隆到 Codex Skill 目录：

```bash
git clone https://github.com/yysfwls/translate-image-to-chinese.git ~/.codex/skills/translate-image-to-chinese
python3 -m pip install -r ~/.codex/skills/translate-image-to-chinese/requirements.txt
```

## 使用

上传需要处理的英文图片，然后输入：

```text
使用 $translate-image-to-chinese 把这张英文配图翻译成中文。
```

若有固定术语偏好，可以同时提供术语表；用户提供的术语表拥有最高优先级。

## 尺寸检查脚本

```bash
python3 scripts/normalize_image_size.py \
  ORIGINAL_IMAGE \
  LOCALIZED_IMAGE \
  --output FINAL_IMAGE
```

脚本只检查和归一化像素尺寸，不参与 OCR、翻译或视觉质量判断。它不会覆盖待检查图片。

## 文件结构

```text
translate-image-to-chinese/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── normalize_image_size.py
└── requirements.txt
```

## 限制

文字特别小、信息密度高或字体效果复杂的图片仍需人工复核。图像编辑结果应检查文字准确性和视觉漂移，不能只依赖自动尺寸校验。
