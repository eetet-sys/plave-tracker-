import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="PLAVE PLLI TRACKER", page_icon="💙", layout="wide")

# 2. 구글 시트 연결
SHEET_ID = "1fO9eZpzP8orgwRkH0FiwO1ZAQmvaKJqpMmophIP_8Ts"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 3. 디자인 CSS (D-Day 배지 스타일 추가)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .main-title { color: #FFFFFF; text-shadow: 2px 2px 10px rgba(162, 155, 254, 0.8); text-align: center; font-size: 2.5rem; font-weight: 800; }
    .tweet-card { background-color: #1E2330; border: 1px solid #3E4556; border-radius: 12px; padding: 20px; margin-bottom: 20px; position: relative; }
    .category-tag { background-color: #A29BFE; color: #0E1117; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; margin-bottom: 10px; display: inline-block; }
    .d-day-tag { float: right; background-color: #FF7675; color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
    .account-name { color: #A29BFE !important; font-weight: bold; }
    .date-info { font-size: 0.8rem; color: #8899A6; margin-bottom: 10px; }
    .tweet-text { color: #E0E0E0 !important; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>💙 PLAVE PLLI TRACKER</h1>", unsafe_allow_html=True)

# 4. 데이터 로드 및 D-Day 계산 함수
try:
    df = pd.read_csv(SHEET_URL)
    
    def get_d_day(end_date_str):
        try:
            end_date = datetime.strptime(str(end_date_str), '%YYYY-%mm-%dd').date()
            today = datetime.now().date()
            delta = (end_date - today).days
            if delta > 0: return f"D-{delta}"
            elif delta == 0: return "D-Day"
            else: return "종료"
        except:
            return "상시"

    def display_cards(data):
        if data.empty:
            st.info("해당 카테고리에 등록된 소식이 없습니다.")
        else:
            cols = st.columns(2)
            for idx, row in data.iterrows():
                d_day_label = get_d_day(row.get('end_date'))
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div class="tweet-card">
                            <span class="category-tag">{row.get('category', '미분류')}</span>
                            <span class="d-day-tag">{d_day_label}</span>
                            <div class="account-name">@{row.get('account', '정보없음')}</div>
                            <div class="date-info">🗓️ {row.get('start_date', '-')} ~ {row.get('end_date', '-')}</div>
                            <div class="tweet-text">{row.get('text', '내용 없음')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if pd.notna(row.get('images')):
                        st.image(row['images'], use_container_width=True)
                    if pd.notna(row.get('link')):
                        st.markdown(f"[🔗 바로가기/참여하기]({row['link']})")
                    st.write("")

    # 탭 메뉴 구성
    tabs = st.tabs(["전체", "🏆 시상식", "🎂 생일", "🗳️ 일반/음방", "🎨 광고시안", "✨ 기타"])
    
    categories = {
        1: '시상식', 2: '생일', 3: ['일반', '음방'], 4: '광고시안'
    }

    with tabs[0]: display_cards(df)
    with tabs[1]: display_cards(df[df['category'] == '시상식'])
    with tabs[2]: display_cards(df[df['category'] == '생일'])
    with tabs[3]: display_cards(df[df['category'].isin(['일반', '음방'])])
    with tabs[4]: display_cards(df[df['category'] == '광고시안'])
    with tabs[5]: display_cards(df[~df['category'].isin(['시상식', '생일', '일반', '음방', '광고시안'])])

except Exception as e:
    st.error(f"데이터 로드 오류: {e}")
