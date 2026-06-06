"""
Translation Agent - AI翻译助手
支持多语言翻译、本地化、术语管理
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class TranslationAgent:
    """
    AI翻译助手
    支持：多语言翻译、术语管理、质量检查
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        self.glossary: Dict[str, Dict[str, str]] = {}
        self.translation_memory: List[Dict] = []

        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def translate(self, text: str, source_lang: str = "auto", target_lang: str = "English", style: str = "natural") -> str:
        """翻译文本"""
        if not self.client:
            return "LLM客户端未配置"

        # 检查术语表
        glossary_text = ""
        if self.glossary:
            terms = []
            for term, translations in self.glossary.items():
                if target_lang in translations:
                    terms.append(f"{term} → {translations[target_lang]}")
            if terms:
                glossary_text = f"\n术语表：\n" + "\n".join(terms)

        prompt = f"""请将以下文本翻译成{target_lang}：

原文：
{text}
{glossary_text}

要求：
1. 翻译准确、自然流畅
2. 使用{style}风格
3. 遵循术语表（如有）
4. 保持原文格式"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        result = response.choices[0].message.content

        # 保存到翻译记忆
        self.translation_memory.append({
            "source": text,
            "target": result,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def batch_translate(self, texts: List[str], target_lang: str = "English") -> List[str]:
        """批量翻译"""
        return [self.translate(text, target_lang=target_lang) for text in texts]

    def add_glossary_term(self, term: str, translations: Dict[str, str]):
        """添加术语"""
        self.glossary[term] = translations

    def check_quality(self, source: str, translation: str, target_lang: str = "English") -> Dict:
        """检查翻译质量"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请评估以下翻译的质量：

原文：{source}
译文：{translation}

请返回JSON格式：
{{
    "score": 1-10,
    "accuracy": "准确性评价",
    "fluency": "流畅度评价",
    "style": "风格评价",
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"quality": content}

    def localize(self, content: str, target_locale: str = "zh-CN") -> str:
        """本地化内容"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请将以下内容本地化为{target_locale}：

{content}

要求：
1. 适应目标地区的文化习惯
2. 调整日期、数字、货币格式
3. 使用当地惯用表达
4. 保持专业性"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def get_stats(self) -> Dict:
        """获取统计"""
        lang_counts = {}
        for mem in self.translation_memory:
            lang = mem.get("target_lang", "unknown")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        return {
            "total_translations": len(self.translation_memory),
            "glossary_terms": len(self.glossary),
            "language_distribution": lang_counts
        }


def create_agent(**kwargs) -> TranslationAgent:
    """创建翻译Agent"""
    return TranslationAgent(**kwargs)


if __name__ == "__main__":
    agent = create_agent()

    # 添加术语
    agent.add_glossary_term("人工智能", {"English": "Artificial Intelligence", "Japanese": "人工知能"})
    agent.add_glossary_term("机器学习", {"English": "Machine Learning", "Japanese": "機械学習"})

    print("Translation Agent")
    print()

    # 测试
    result = agent.translate("人工智能正在改变世界", target_lang="English")
    print(f"Translation: {result}")

    quality = agent.check_quality("人工智能正在改变世界", result)
    print(f"Quality: {quality}")
