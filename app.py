
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import os
from dotenv import load_dotenv

# .envからAPIキーを読み込む
load_dotenv()

# LLM応答取得関数
def get_llm_response(user_input: str, expert_type: str) -> str:
	if expert_type == "A":
		system_message = "あなたは音楽の専門家です。音楽に関する質問には専門的な知識で答えてください。"
	elif expert_type == "B":
		system_message = "あなたはサッカーの専門家です。サッカーに関する質問には専門的な知識で答えてください。"
	else:
		system_message = "あなたは親切なアシスタントです。"

	prompt = ChatPromptTemplate.from_messages([
		SystemMessagePromptTemplate.from_template(system_message),
		HumanMessagePromptTemplate.from_template("{input}")
	])

	llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
	chain = prompt | llm
	response = chain.invoke({"input": user_input})
	return response.content

# --- Streamlit UI ---
st.title("専門家LLMチャットアプリ")

st.markdown("""
このアプリは、入力したテキストに対してLLM（大規模言語モデル）が専門家として回答します。\
ラジオボタンで「音楽の専門家」または「サッカーの専門家」を選択し、質問を入力してください。\
送信ボタンを押すと、選択した専門家になりきったLLMの回答が表示されます。
""")

expert_type = st.radio(
	"専門家の種類を選択してください:",
	("A", "B"),
	format_func=lambda x: "音楽の専門家 (A)" if x == "A" else "サッカーの専門家 (B)"
)

user_input = st.text_area("質問を入力してください:")

if st.button("送信"):
	if user_input.strip() == "":
		st.warning("質問を入力してください。")
	else:
		with st.spinner("LLMが回答中..."):
			answer = get_llm_response(user_input, expert_type)
		st.markdown("#### 回答")
		st.success(answer)
from dotenv import load_dotenv

load_dotenv()
