import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 및 제목 (여행 테마)
st.set_page_config(page_title="AI 여행 가이드", page_icon="✈️")
st.title("✈️ AI 여행 플래너: 트리피(Trippy)")
st.write(
    "어디로 떠나고 싶으신가요? 목적지 추천부터 맛집, 일정 짜기까지 "
    "당신의 완벽한 여행을 도와드려요! 🌍"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("여행을 시작하려면 OpenAI API 키를 입력해 주세요. 🗝️", icon="📍")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 저장 (시스템 메시지 포함)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": (
                    "너는 친절하고 전문적인 여행 가이드야. "
                    "사용자의 취향(휴양, 관광, 미식 등)에 맞춰 최적의 여행지와 일정을 추천해줘. "
                    "답변할 때는 해당 지역의 날씨 팁이나 필수 준비물도 함께 알려주면 좋아."
                )
            }
        ]

    # 채팅 기록 표시 (시스템 메시지는 제외하고 표시)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("예: 3월에 가기 좋은 일본 온천 여행지 추천해줘!"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API 호출
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo", # 더 정확한 답변을 원하시면 "gpt-4-turbo" 권장
            messages=st.session_state.messages,
            stream=True,
        )

        # 어시스턴트 답변 생성 및 스트리밍
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
