import json
import logging
import re

from anthropic import Anthropic

from app.config import settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are a CV parsing expert for a consulting firm. Extract structured information from the provided CV text.

Return ONLY a valid JSON object with these fields:
{
  "name": "Full name (use the hint if not found in text)",
  "skills": ["technical skills, tools, frameworks, platforms"],
  "certifications": ["official certifications, e.g. AZ-900, AWS Solutions Architect"],
  "experience_summary": "2-3 sentence summary of their professional experience",
  "domains": ["domain expertise, e.g. cloud computing, data engineering, machine learning"],
  "languages": ["programming languages AND spoken languages"],
  "education": "highest degree and institution",
  "years_of_experience": <integer or null>
}

Be thorough with skills — include all mentioned technologies, tools, and platforms.
Do not include markdown, only return raw JSON.\
"""


def parse_profile_with_claude(raw_text: str, name_hint: str) -> dict:
    """Call Claude to parse raw CV text into structured profile fields."""
    client = Anthropic(api_key=settings.anthropic_api_key)

    truncated_text = raw_text[:8000]

    try:
        response = client.messages.create(
            model=settings.llm_model,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Name hint (from filename): {name_hint}\n\n"
                        f"CV Text:\n{truncated_text}"
                    ),
                }
            ],
        )

        content = response.content[0].text.strip()

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(content)

    except Exception as e:
        logger.error(f"Claude profile parsing failed for '{name_hint}': {e}")
        return {
            "name": name_hint,
            "skills": [],
            "certifications": [],
            "experience_summary": raw_text[:400],
            "domains": [],
            "languages": [],
            "education": "",
            "years_of_experience": None,
        }
