"""
Simple web app: judge whether to stay emotionally stable in the given intimate-relationship situation.
Uses OpenAI API with strict Y/N output.
Base URL: /emo
"""
import os
import re
from flask import Flask, Blueprint, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 所有路由挂载在 base url /emo 下
emo_bp = Blueprint(
    "emo",
    __name__,
    url_prefix="/emo",
    static_folder="static",
    static_url_path="static",
)

# Detailed English prompt, low temperature for consistent Y/N only.
STABILITY_PROMPT = """You are an expert in intimate relationships and emotional regulation.

Task: Given a situation described by the user that occurs within an intimate relationship (romantic, family, or close friendship), determine whether the person in that situation SHOULD maintain emotional stability (stay calm, not react with strong negative emotion, avoid escalation).

Rules:
- Answer ONLY with a single letter: Y or N.
- Y = Yes, they should maintain emotional stability in this situation.
- N = No, it is reasonable or healthy in this situation to express emotion or not prioritize staying calm (e.g. clear boundary-setting, leaving abuse, justified anger at betrayal).
- Consider: Is staying "emotionally stable" here beneficial for the relationship and the person? Would suppressing emotion be harmful? Is this a situation where calm response is appropriate?
- Do not output any other text, explanation, or punctuation. Only the letter Y or N."""


def normalize_answer(text: str) -> str:
    """Extract Y or N from model output."""
    if not text:
        return "N"
    s = text.strip().upper()
    if s.startswith("Y") or s == "Y":
        return "Y"
    return "N"


@emo_bp.route("/")
def index():
    return render_template("index.html")


@emo_bp.route("/api/judge", methods=["POST"])
def judge():
    data = request.get_json() or {}
    situation = (data.get("situation") or "").strip()
    if not situation:
        return jsonify({"error": "situation is required", "answer": None}), 400

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENAI_API_KEY not configured", "answer": None}), 503

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": STABILITY_PROMPT},
                {"role": "user", "content": situation},
            ],
            temperature=0,
            max_completion_tokens=5,
            seed=42,
        )
        raw = (response.choices[0].message.content or "").strip()
        answer = normalize_answer(raw)
        return jsonify({"answer": answer, "raw": raw})
    except Exception as e:
        return jsonify({"error": str(e), "answer": None}), 500


app.register_blueprint(emo_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 13942)))
