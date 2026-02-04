import streamlit as st
import json

# 1. 페이지 설정 및 테마 컬러 정의
st.set_page_config(
    page_title="PLAVE PLLI Dashboard",
    page_icon="💙",
    layout="wide"
)

# 플레이브 스타일 CSS 주입
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
        color: #E0E0E0;
    }
    .tweet-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out;
    }
    .tweet-card:hover {
        transform: translateY(-5px);
        border-color: #A29BFE;
        background-color: rgba(255, 255, 255, 0.08);
    }
    .account-name {
        color: #A29BFE;
        font-weight: bold;
        font-size: 1.1em;
    }
    .tweet-text {
        color: #FFFFFF;
        line-height: 1.6;
    }
    h1 {
        color: #FFFFFF;
        text-shadow: 0 0 10px rgba(162, 155, 254, 0.8);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 헤더 섹션
st.markdown("<h1>💙 PLAVE VOTE & AD TRACKER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A29BFE;'>Asterum의 소식을 실시간으로 확인하세요</p>", unsafe_allow_html=True)

# 3. 데이터 로드 및 출력 (try 문 안에 모든 로직을 포함)
try:
    with open('plave_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 상단 요약 바
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("수집된 정보", f"{len(data)}개")
    with col2:
        st.metric("타겟 계정", "28개")
    with col3:
        if st.button('✨ 최신 데이터로 새로고침'):
            st.rerun()

    st.divider()

    # 4. 카드 형태 레이아웃 출력
    if not data:
        st.markdown("""
            <div style='text-align: center; padding: 50px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px dashed #A29BFE;'>
                <h2 style='color: #A29BFE;'>💫 아스테룸의 주파수가 잠잠합니다</h2>
                <p style='color: #E0E0E0;'>현재 수집된 새로운 투표나 광고 시안 소식이 없습니다.<br>잠시 후 다시 확인해 주세요!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for idx, item in enumerate(data):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="tweet-card">
                        <span class="account-name">@{item['account']}</span>
                        <p style="font-size: 0.8em; color: #888;">{item['date']}</p>
                        <p class="tweet-text">{item['text']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if item.get('images'):
                    st.image(item['images'][0], use_container_width=True)
                
                st.markdown(f"[🔗 트윗 원문 보기]({item['link']})")
                st.write("") 

except FileNotFoundError:
    st.info("💙 첫 번째 데이터를 수집 중입니다. GitHub Actions를 확인해 주세요!")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
