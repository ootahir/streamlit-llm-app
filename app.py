from dotenv import load_dotenv

load_dotenv()
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ----------------------------------------
# LLM 初期化
# ----------------------------------------
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

st.title("専門家切替 LLM チャット")

# ----------------------------------------
# 専門家選択ラジオボタン
# ----------------------------------------
expert_choice = st.radio(
    "LLMに振る舞わせる専門家を選択してください",
    options=("A: 薬の専門家", "B: 英語教師")
)

# ラジオボタンの選択値から SystemMessage を作成
if expert_choice.startswith("A"):
    system_prompt = (
        "あなたは薬の専門家（薬剤師）として振る舞います。"
        "薬の作用、副作用、相互作用、服薬方法などについて、"
        "安全に配慮しながら、分かりやすく専門的に説明してください。"
    )
else:
    system_prompt = (
        "あなたは英語教師として振る舞います。"
        "英文法、語彙、表現のニュアンスを、日本語を交えて"
        "分かりやすく説明し、必要に応じて例文を示してください。"
    )

# ----------------------------------------
# 入力フォーム（1つ）
# ----------------------------------------
user_input = st.text_area(
    "質問を入力してください",
    height=120,
    placeholder="例: 日本の首都を教えてください。"
)

# ----------------------------------------
# 送信処理
# ----------------------------------------
if st.button("送信"):
    if not user_input.strip():
        st.warning("テキストを入力してください。")
    else:
        try:
            # LangChain メッセージ構築（ご提示サンプルを踏襲）
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input),
            ]

            # LLM 実行
            with st.spinner("回答を生成中..."):
                result = llm.invoke(messages)

            # 結果表示
            st.markdown("## 回答")
            st.write(result.content)
        
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.info("APIキーが正しく設定されているか、.envファイルを確認してください。")
