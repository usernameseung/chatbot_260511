import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 (귀여운 아이콘과 타이틀)
st.set_page_config(
    page_title="냠냠서울 | 나만의 맛집 메이트",
    page_icon="🍭",
    layout="centered"
)

# 2. 귀여운 UI를 위한 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경색 - 연한 핑크/크림 */
    .stApp {
        background-color: #FFF5F7;
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #FF85A2;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px #FFD1DC;
    }
    
    /* 설명 문구 스타일 */
    .sub-title {
        text-align: center;
        color: #FFB3C1;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* 채팅 메시지 박스 둥글게 */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    
    /* 사용자 메시지 (연한 블루) */
    [data-testid="stChatMessageUser"] {
        background-color: #E3F2FD !important;
        border: 2px solid #BBDEFB;
    }
    
    /* 봇 메시지 (연한 핑크) */
    [data-testid="stChatMessageAssistant"] {
        background-color: #FFEBEE !important;
        border: 2px solid #FFCDD2;
    }

    /* 입력창 디자인 */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 2px solid #FFB3C1 !important;
        background-color: white !important;
    }

    /* 버튼 스타일 */
    button {
        border-radius: 20px !important;
        background-color: #FF85A2 !important;
        color: white !important;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #FFFAFB;
        border-right: 2px dashed #FFD1DC;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 - 귀여운 필터링
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FF85A2;'>🎀 필터링 🎀</h2>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/bubbles/200/restaurant.png", use_container_width=True)
    
    openai_api_key = st.text_input("OpenAI 키를 넣어줘!", type="password", placeholder="sk-...")
    
    st.divider()
    
    st.markdown("**어디로 갈까? 📍**")
    area = st.selectbox("서울 지역 선택", ["강남구", "마포구(홍대)", "성동구(성수)", "용산구(한남)", "종로구", "송파구"])
    
    st.markdown("**어떤 음식이 당겨? 🍰**")
    mood = st.select_slider("오늘의 분위기", options=["가성비", "적당함", "분위기 갑", "럭셔리"])
    
    st.write("---")
    st.caption("냠냠서울 v1.0 | 만든이: 귀염둥이 개발자")

# 4. 메인 화면 헤더
st.markdown("<p class='main-title'>🍭 냠냠서울</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>오늘 점심 뭐 먹지? 내가 딱 정해줄게! ✨</p>", unsafe_allow_html=True)

# 5. 로직 시작
if not openai_api_key:
    st.info("왼쪽 주머니(사이드바)에 API 키를 쏙 넣어주면 맛집 여행을 시작할 수 있어! 🗝️", icon="🍬")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 세션 메시지 초기화 (페르소나: 귀여운 미식가 친구)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "너는 서울의 모든 맛집을 섭렵한 귀여운 미식가 친구 '냠냠이'야. "
                "말투는 매우 친절하고 귀여워야 해. (~했어용, ~해봐요!, ✨, 💖 같은 이모지 다수 사용) "
                "답변은 다음 형식을 꼭 지켜줘:\n"
                "1. 식당 이름 (귀여운 이모지와 함께)\n"
                "2. 왜 추천하는지 (맛이나 분위기)\n"
                "3. 추천 메뉴와 꿀팁\n"
                "항상 사용자의 선택된 지역과 분위기를 참고해서 알려줘!"
            )
        }
    ]

# 채팅 기록 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "🍭"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# 6. 채팅 입력 및 응답
if prompt := st.chat_input("먹고 싶은 거나 궁금한 거 물어봐! (예: 떡볶이 맛집 알려줘)"):
    
    # 필터 정보를 섞어서 질문 생성
    refined_prompt = f"[지역:{area} / 분위기:{mood}] {prompt}"
    
    st.session_state.messages.append({"role": "user", "content": refined_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🍭"):
        with st.spinner("냠냠이가 맛집 지도 뒤지는 중... 🐾"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
