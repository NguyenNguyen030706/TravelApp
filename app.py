import streamlit as st
import json
import re
import ollama

# Cấu hình API base (Ollama local trên Windows/Mac/Linux)
ollama.api_base = "http://127.0.0.1:11434"

# ---------------- Login ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "user" and password == "123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Logged in!")
        else:
            st.error("❌ Invalid credentials")

else:
    st.title("🌍 Travel Itinerary Generator")

    origin = st.text_input("Origin city")
    destination = st.text_input("Destination city")
    dates = st.text_input("Travel dates (e.g., 2025-11-10 to 2025-11-15)")
    interests = st.multiselect("Interests", ["food", "museums", "nature", "nightlife"])
    pace = st.radio("Travel pace", ["relaxed", "normal", "tight"])

    if st.button("Generate Itinerary"):

        # ✅ Prompt buộc LLM trả JSON hợp lệ
        prompt = f"""
You MUST return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Return a JSON object in this exact structure:
{{
  "Day 1": {{
    "morning": "activity",
    "afternoon": "activity",
    "evening": "activity"
  }},
  "Day 2": {{
    "morning": "activity",
    "afternoon": "activity",
    "evening": "activity"
  }}
}}

Trip details:
Origin: {origin}
Destination: {destination}
Dates: {dates}
Interests: {', '.join(interests)}
Pace: {pace}
"""

        # ✅ Gọi model Ollama local
        try:
            result = ollama.chat(
                model="llama2",
                messages=[{"role": "user", "content": prompt}]
            )
            text = result["message"]["content"]
        except Exception as e:
            st.error(f"❌ Ollama error: {e}")
            text = "{}"

        # ✅ Lọc JSON cho chắc chắn
        try:
            json_str = re.search(r"\{.*\}", text, re.DOTALL).group(0)
            itinerary = json.loads(json_str)
        except Exception as e:
            st.error(f"⚠️ Failed to parse JSON: {e}")
            itinerary = {}

        # ✅ Hiển thị lịch trình
        st.subheader("✅ Your Itinerary")
        for day, plan in itinerary.items():
            st.markdown(f"### {day}")
            for time, act in plan.items():
                st.markdown(f"- **{time}**: {act}")

        # ✅ Lưu lịch sử
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
        except:
            history = []

        history.append({
            "user": st.session_state.username,
            "input": {
                "origin": origin,
                "destination": destination,
                "dates": dates,
                "interests": interests,
                "pace": pace
            },
            "itinerary": itinerary
        })

        with open("history.json", "w") as f:
            json.dump(history, f, indent=2)

    # ✅ Hiển thị lịch sử
    if st.checkbox("Show history"):
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
            for chat in history:
                if chat["user"] == st.session_state.username:
                    st.write(chat)
        except:
            st.info("No history yet.")
