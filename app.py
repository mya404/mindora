from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

try:
    from google import genai
except ImportError:  # pragma: no cover - installed on deploy.
    genai = None


Mood = Literal["stressed", "anxious", "lonely", "sad", "calm", "crisis"]
analyzer = SentimentIntensityAnalyzer()


@dataclass(frozen=True)
class ChatReply:
    mood: Mood
    mood_label: str
    summary: str
    response: str
    tip: str


KEYWORDS: dict[Mood, tuple[str, ...]] = {
    "stressed": ("stress", "stressed", "deadline", "assignments", "overwhelmed"),
    "anxious": ("anxious", "anxiety", "panic", "worried", "nervous", "racing thoughts"),
    "lonely": ("lonely", "alone", "isolated", "left out", "nobody"),
    "sad": ("sad", "down", "empty", "hopeless", "tired", "unmotivated"),
    "calm": ("good", "better", "okay", "ok", "calm", "relieved", "safe"),
    "crisis": ("suicide", "kill myself", "end it", "hurt myself", "self-harm", "can't go on"),
}

LABELS = {
    "stressed": "Stress",
    "anxious": "Anxiety",
    "lonely": "Loneliness",
    "sad": "Low mood",
    "calm": "Balanced",
    "crisis": "Crisis support",
}

SUMMARIES = {
    "stressed": "The message reads like school pressure or overload.",
    "anxious": "The message suggests worry, restlessness, or racing thoughts.",
    "lonely": "The message points to a need for connection.",
    "sad": "The message suggests sadness or low energy.",
    "calm": "The message feels fairly steady or neutral.",
    "crisis": "The message sounds urgent and safety-related.",
}

TIPS = {
    "stressed": "Pick one tiny task you can finish in 10 minutes.",
    "anxious": "Breathe in for 4, hold for 4, and breathe out for 6.",
    "lonely": "Send one short message to someone you trust.",
    "sad": "Stand up, stretch once, and drink some water.",
    "calm": "Keep the steady pace going and do one small thing for yourself.",
    "crisis": "Please contact local emergency services or a trusted person right now.",
}


def get_api_key() -> str:
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        return ""


def detect_mood(text: str) -> Mood:
    lowered = text.lower()
    if any(term in lowered for term in KEYWORDS["crisis"]):
        return "crisis"

    scores = {
        mood: sum(1 for term in terms if term in lowered)
        for mood, terms in KEYWORDS.items()
        if mood != "crisis"
    }
    if any(scores.values()):
        return max(scores, key=scores.get)

    compound = analyzer.polarity_scores(text)["compound"]
    if compound >= 0.35:
        return "calm"
    if compound <= -0.45:
        return "sad"
    if compound <= -0.2:
        return "stressed"
    return "calm"


def fallback_reply(mood: Mood) -> str:
    return {
        "stressed": "That sounds like a lot. Take the smallest next step, not the whole list.",
        "anxious": "That sounds tense and uncomfortable. Let’s slow it down and breathe first.",
        "lonely": "Feeling disconnected can hurt. One small message can be a good first step.",
        "sad": "I’m sorry this feels so low right now. Try one small reset and be gentle with yourself.",
        "calm": "Thanks for sharing that. I’m here with you.",
        "crisis": "I’m really glad you said that. Please contact emergency services or a trusted person immediately.",
    }[mood]


def build_reply(text: str) -> ChatReply:
    mood = detect_mood(text)
    summary = SUMMARIES[mood]

    if mood == "crisis":
        return ChatReply(mood, LABELS[mood], summary, fallback_reply(mood), TIPS[mood])

    response = fallback_reply(mood)
    key = get_api_key()
    if key and genai is not None:
        try:
            client = genai.Client(api_key=key)
            prompt = (
                "You are a warm student mental health chatbot. Reply in 2 short paragraphs. "
                f"Mood: {mood}. Summary: {summary}. Message: {text}"
            )
            result = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            generated = getattr(result, "text", "").strip()
            if generated:
                response = generated
        except Exception:
            pass

    return ChatReply(mood, LABELS[mood], summary, response, TIPS[mood])


def ensure_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I’m Mindora. Tell me how your day feels and I’ll try to help."}
        ]


def main() -> None:
    st.set_page_config(page_title="Mindora", page_icon="💬", layout="centered")

    st.title("Mindora")
    st.caption("A simple student mental health companion chatbot.")

    if not get_api_key():
        st.info("Set GEMINI_API_KEY in Streamlit Secrets before deploying.")

    ensure_state()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Tell me what is on your mind...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply = build_reply(prompt)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Mood: {reply.mood_label}\n\n{reply.response}\n\nTip: {reply.tip}",
            }
        )
        st.rerun()


if __name__ == "__main__":
    main()