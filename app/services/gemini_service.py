"""
Gemini AI Service
Generates personalized lesson content using Gemini 2.5 Flash
"""

import httpx
import json
from app.config import settings


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


async def generate_lesson_content(
    topic: str,
    learning_style: str,
    difficulty: str,
    user_name: str = "Student",
    cognitive_capacity: float = 7.0
) -> dict:
    """Generate personalized lesson content using Gemini 2.5 Flash"""

    prompt = f"""
You are an expert adaptive learning AI for NeuroLearn.

Generate a complete, engaging lesson for:
- Topic: {topic}
- Student: {user_name}
- Learning Style: {learning_style} (visual/auditory/kinesthetic/reading_writing)
- Difficulty: {difficulty}
- Cognitive Capacity: {cognitive_capacity}/10

Return ONLY valid JSON in this exact format:
{{
    "title": "Lesson title",
    "module": "Module name",
    "duration_minutes": 30,
    "objectives": ["objective 1", "objective 2", "objective 3"],
    "sections": [
        {{
            "heading": "Section title",
            "content": "Detailed explanation paragraph...",
            "code_example": "# Python code here or null if not applicable",
            "key_point": "One key takeaway from this section"
        }}
    ],
    "quiz": [
        {{
            "question": "Question text?",
            "options": ["A", "B", "C", "D"],
            "correct": 0,
            "explanation": "Why this answer is correct"
        }}
    ],
    "summary": "Brief summary of what was learned",
    "next_topic": "Suggested next topic to learn"
}}

Adapt content for {learning_style} learners:
- visual: include diagram descriptions, charts, visual metaphors
- kinesthetic: include hands-on exercises, interactive examples
- reading_writing: include detailed text, notes, definitions
- auditory: include explanations as if spoken, mnemonics

Make it engaging and appropriately challenging for {difficulty} level.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload
        )
        response.raise_for_status()
        result = response.json()

    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
    lesson_data = json.loads(raw_text)
    return lesson_data


async def generate_quiz_feedback(
    question: str,
    user_answer: int,
    correct_answer: int,
    explanation: str,
    learning_style: str
) -> str:
    """Generate personalized feedback for quiz answers"""

    is_correct = user_answer == correct_answer

    prompt = f"""
Student answered a quiz question {'correctly' if is_correct else 'incorrectly'}.

Question: {question}
Their answer was {'correct' if is_correct else 'wrong'}.
Explanation: {explanation}
Learning style: {learning_style}

Give brief, encouraging feedback (2-3 sentences max) adapted for
a {learning_style} learner. Be positive and educational.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 200
        }
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload
        )
        response.raise_for_status()
        result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]