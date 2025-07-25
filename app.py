import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pathlib import Path

# .envからOPENAI_API_KEYを読み込む
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')


# LangChainのChatモデルを準備
llm = ChatOpenAI(temperature=0.7)

# 専門家のシステムメッセージを定義
EXPERT_MESSAGES = {
    "doctor": "あなたは優秀な医師です。症状や病状について分かりやすく丁寧に説明してください。",
    "lawyer": "あなたは経験豊富な弁護士です。法的な質問に分かりやすく正確に答えてください。",
    "engineer": "あなたは熟練のソフトウェアエンジニアです。技術的な質問に的確に答えてください。",
}

# LLMからの回答を返す関数
def get_expert_response(user_input: str, expert_type: str) -> str:
    if expert_type not in EXPERT_MESSAGES:
        raise ValueError(f"未定義の専門家タイプです: {expert_type}")
    system_prompt = EXPERT_MESSAGES[expert_type]
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    try:
        response = llm.invoke(messages)
        if hasattr(response, "content"):
            return response.content
        else:
            return "AIからの回答を取得できませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Webアプリ本体
st.set_page_config(page_title="専門家チャット", layout="centered")

st.title("💬 専門家チャットBot")
st.markdown("以下のフォームに質問や相談を入力し、相談したい専門家の種類を選んでください。選ばれた専門家の立場でAIが回答します。")

# 入力欄
user_input = st.text_area("ご相談内容を入力してください:", height=150)

# 専門家タイプの表示名辞書
EXPERT_TYPE_DISPLAY = {
    "doctor": "医師",
    "lawyer": "弁護士",
    "engineer": "エンジニア"
}

# ラジオボタン（専門家の選択）
expert_type = st.radio(
    "専門家の種類を選択してください:",
    options=["doctor", "lawyer", "engineer"],
    format_func=lambda x: EXPERT_TYPE_DISPLAY[x]
)

# 送信ボタン
if st.button("相談する"):
    if user_input.strip():
        with st.spinner("専門家に相談中..."):
            try:
                answer = get_expert_response(user_input, expert_type)
                st.success("回答:")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("相談内容を入力してください。")