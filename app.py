import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="PLAVE PLLI Dashboard",
    page_icon="💙",
    layout="wide"
)

# 2. 구글 시트 연결 설정 (보내주신 ID 적용)
SHEET_ID = "1fO9eZpzP8orgwRkH0FiwO1ZAQmvaKJqpMmophIP_8Ts"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 3. 디자인 CSS
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

# 4. 헤더 섹션
st.markdown("<h1 class='main-title'>💙 PLAVE VOTE & AD TRACKER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A29BFE; font-weight: 500;'>구글 시트와 동기화된 투표 정보입니다</p>", unsafe_allow_html=True)

# 5. 데이터 로드 및 출력
try:
    # 구글 시트 데이터 읽기
    df = pd.read_csv(SHEET_URL)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("수집된 정보", f"{len(df)}개")
    with col2:
        st.metric("연동 상태", "실시간")
    with col3:
        if st.button('✨ 데이터 새로고침'):
            st.cache_data.clear()
            st.rerun()

    st.divider()

    if df.empty:
        st.info("💫 구글 시트에 데이터를 입력해 주세요! (첫 줄은 account, text, date, link, images)")
    else:
        # 2열로 배치
        cols = st.columns(2)
        for idx, row in df.iterrows():
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="tweet-card">
                        <div class="account-name">@{row.get('account', 'Unknown')}</div>
                        <div style="font-size: 0.8rem; color: #8899A6; margin-bottom: 10px;">{row.get('date', '-')}</div>
                        <div class="tweet-text">{row.get('text', '내용 없음')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 이미지가 있는 경우 (구글 드라이브나 웹 이미지 링크)
                if pd.notna(row.get('images')):
                    st.image(row['images'], use_container_width=True)
                
                # 원문 링크가 있는 경우
                if pd.notna(row.get('link')):
                    st.markdown(f"[🔗 원문 보기]({row['link']})")
                st.write("")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다. 시트의 [공유] 설정이 '링크가 있는 모든 사용자'로 되어 있는지 확인해 주세요! \n\n 오류 내용: {e}")
