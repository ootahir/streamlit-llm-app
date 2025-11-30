from dotenv import load_dotenv

load_dotenv()
import os
from google.colab import userdata

os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
!pip install langchain==0.3.26 openai==1.91.0 langchain-community==0.3.26 langchain-openai==0.3.27 httpx==0.28.1
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# -----------------------------
# LLM 呼び出し用関数
# -----------------------------
def ask_llm(user_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプ(A or B)を受け取り、
    LLMからの回答テキストを返す。
    """

    # 専門家タイプによって SystemMessage を切り替え
    if expert_type == "A":
        system_prompt = (
            "あなたは日本の薬剤師として振る舞います。"
            "患者の症状や処方薬について、薬理作用、副作用、"
            "相互作用、服薬指導などを分かりやすく、専門的に説明してください。"
            "医療安全や薬機法を意識し、適切な助言を行ってください。"
        )
    elif expert_type == "B":
        system_prompt = (
            "あなたは日本人学習者向けの英語教師として振る舞います。"
            "英文法、語彙、発音、表現のニュアンスを、日本語を交えて"
            "わかりやすく解説してください。"
            "必要に応じて例文を提示してください。"
        )
    else:
        raise ValueError("expert_type には 'A' または 'B' を指定してください。")

    # LLM インスタンス
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # LangChain メッセージ作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]

    # モデル実行
    result = llm(messages)

    # 生成テキストを返却
    return result.content


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("専門家切り替え LLM チャット")

# ラジオボタン（A / B）
choice_label = st.radio(
    "LLMに振る舞わせる専門家を選択してください",
    ("A: 薬剤師", "B: 英語教師")
)

# 表示ラベル → 内部値へ変換
expert_type = "A" if choice_label.startswith("A") else "B"

# 入力欄
user_input = st.text_area("質問を入力してください", height=150)

# 実行ボタン
if st.button("送信"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        # -----------------------------
        # 定義した関数を利用
        # -----------------------------
        answer = ask_llm(user_input, expert_type)

        # 結果表示
        st.markdown("## 回答")
        st.write(answer)