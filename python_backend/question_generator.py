import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
BANK_FILE = ROOT / "question_bank.json"
OUTPUT_FILE = ROOT / "selected_questions.json"

def generate_questions(domain, level, num_questions=5):
    data = json.loads(BANK_FILE.read_text(encoding="utf-8"))

    if domain not in data or level not in data[domain]:
        raise ValueError("No questions available for selected domain/level")

    questions_pool = data[domain][level]
    selected = random.sample(questions_pool, min(num_questions, len(questions_pool)))

    payload = {
        "domain": domain,
        "level": level,
        "questions": selected
    }

    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return selected
