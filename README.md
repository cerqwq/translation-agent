# 🌐 Translation Agent

AI翻译助手，支持多语言翻译、本地化、术语管理。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🌍 多语言翻译
- 📚 术语表管理
- 🔄 翻译记忆
- ✅ 质量检查
- 🌐 本地化支持

## 🚀 快速开始

```bash
pip install openai

python agent.py
```

## 📖 使用

```python
from translation_agent import create_agent

agent = create_agent()

# 添加术语
agent.add_glossary_term("人工智能", {"English": "AI", "Japanese": "人工知能"})

# 翻译
result = agent.translate("人工智能改变世界", target_lang="English")

# 批量翻译
results = agent.batch_translate(["文本1", "文本2"], "English")

# 质量检查
quality = agent.check_quality(source, translation)

# 本地化
localized = agent.localize(content, "zh-CN")
```

## 📁 项目结构

```
translation-agent/
├── agent.py       # 翻译Agent核心
└── README.md
```

## 📄 许可证

MIT License
