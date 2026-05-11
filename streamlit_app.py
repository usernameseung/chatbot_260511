import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 (브라우저 탭 및 레이아웃)
st.set_page_config(
    page_title="맛플레이스 SEOUL | 서울 맛집 큐레이션",
    page_icon="🍴",
    layout="wide"
)

# 2. 커스텀 CSS (음식 플랫폼 느낌의 디자인)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .st-emotion-cache-1c7n2ka {
        background-color: #ffffff;
        border: 1px solid #ff4b4b;
    }
    h1 {
        color: #ff4b4b;
        font-family: 'Pretendard', sans-serif;
    }
    .sidebar-text {
        font-size: 14px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 - 설정 및 필터
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80", use_container_width=True)
    st.title("🍔 맛플레이스 설정")
    
    openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    st.divider()
    
    st.subheader("📍 선호 지역")
    location = st.multiselect("어디로 가시나요?", 
                             ["강남/역삼", "홍대/연남", "성수/서울숲", "을지로/종로", "한남/이태원", "잠실/송파"],
                             default=["강남/역삼"])
    
    st.subheader("🍱 음식 종류")
    food_type = st.radio("오늘의 메뉴는?", 
                        ["전체", "한식", "일식", "양식", "중식", "디저트/카페"])
    
    st.info("💡 팁: '성수동 분위기 좋은 와인바 추천해줘'라고 물어보세요!")

# 4. 메인 화면 헤더
st.title("🍴 서울 맛집 큐레이터")
st.caption("실시간 트렌드와 사용자 취향을 반영한 서울 최적의 맛집을 추천합니다.")

# 5. 로직 시작
if not openai_api_key:
    st.warning("왼쪽 사이드바에 OpenAI API 키를 입력해 주세요.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 세션 메시지 초기화 (시스템 프롬프트 강화)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "너는 서울 최고의 음식 평론가이자 맛집 큐레이터야. "
                "사용자의 질문에 대해 다음 형식을 지켜서 답변해줘:\n"
                "1. 식당 이름 및 한줄 평\n"
                "2. 추천 메뉴 및 가격대\n"
                "3. 위치 및 특징 (분위기, 웨이팅 팁 등)\n"
                "4. 네이버 지도나 캐치테이블에서 검색해보라는 조언\n"
                "친절하고 맛깔나는 문체를 사용하고, 서울 지역에 특화된 정보를 제공해."
            )
        }
    ]

# 채팅 기록 출력
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. 채팅 입력 및 응답
if prompt := st.chat_input("맛집 정보를 입력하세요 (예: 강남역 조용한 일식집)"):
    
    # 지역/음식 필터 정보를 프롬프트에 결합
    refined_prompt = f"[{', '.join(location)} 지역 / {food_type} 위주] {prompt}"
    
    st.session_state.messages.append({"role": "user", "content": refined_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 로딩 애니메이션
        with st.spinner("서울 시내 맛집을 검색 중입니다..."):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
