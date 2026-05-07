import httpx
async def get_ai_suggestions(
    missing_skills: list,
    job_description: str
) -> list:
    prompt = f"""You are a resume improvement assistant.

The candidate is MISSING these skills from their resume: {', '.join(missing_skills)}

Write exactly 5 suggestions to help them ADD these missing skills to their resume.
Each suggestion must tell them to ADD or LEARN something — not remove anything.
Keep each suggestion under 15 words.

Format EXACTLY like this:
1. Add [skill] experience by building a project using it.
2. Learn [skill] through online courses and add it to skills section.

Only write 5 suggestions. Do not remove any skills. Do not mention cloud or unrelated tools."""

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma:2b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            data = response.json()
            raw = data.get("response", "")

            suggestions = []
            for line in raw.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line[0].isdigit() and "." in line:
                    clean = line.split(".", 1)[-1].strip()
                    if clean:
                        suggestions.append(clean)

            if len(suggestions) == 0:
                suggestions = [s.strip() for s in raw.split("\n") if s.strip()]

            return suggestions[:5]

    except Exception as e:
        return [f"AI suggestions unavailable: {str(e)}"]