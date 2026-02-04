import streamlit as st
import json

# 1. 페이지 설정
st.set_page_config(
    page_title="PLAVE PLLI Dashboard",
    page_icon="💙",
    layout="wide"
)

# 2. 가독성 개선 플레이브 테마 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .main-title {
        color: #FFFFFF;
        text-shadow: 2px 2px 10px rgba(162, 155, 254, 0.8);
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .tweet-card {
        background-color: #1E2330;
        border: 1px solid #3E4556;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .account-name {
        color: #A29BFE !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .tweet-text {
        color: #E0E0E0 !important;
        line-height: 1.6;
        font-size: 1rem;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    [data-testid="stMetricLabel"] {
        color: #A29BFE !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.markdown("<h1 class='main-title'>💙 PLAVE VOTE & AD TRACKER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A29BFE; font-weight: 500;'>Asterum의 소식을 실시간으로 확인하세요</p>", unsafe_allow_html=True)

# 4. 데이터 로드
try:
    # 파일이 있는지 먼저 확인
    with open('plave_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("수집된 정보", f"{len(data)}개")
    with col2:
        st.metric("타겟 계정", "28개")
    with col3:
        if st.button('✨ 데이터 새로고침'):
            st.rerun()

    st.divider()

    if not data:
        st.markdown("""
            <div style='text-align: center; padding: 50px; border: 1px dashed #A29BFE; border-radius: 15px;'>
                <h2 style='color: #A29BFE;'>💫 아스테룸의 주파수가 잠잠합니다</h2>
                <p style='color: #FFFFFF;'>현재 새로운 투표나 시안 소식이 없습니다. <br> 잠시 후 다시 확인해 주세요!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for idx, item in enumerate(data):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="tweet-card">
                        <div class="account-name">@{item['account']}</div>
                        <div style="font-size: 0.8rem; color: #8899A6; margin-bottom: 10px;">{item['date']}</div>
                        <div class="tweet-text">{item['text']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if item.get('images'):
                    st.image(item['images'][0], use_container_width=True)
                
                st.markdown(f"[🔗 트윗 원문 보기]({item['link']})")
                st.write("")

except FileNotFoundError:
    st.info("💙 데이터 파일을 생성 중입니다. GitHub Actions를 실행해 주세요!")
except Exception as e:
    st.error(f"오류 발생: {e}")
