import streamlit as st
import json

st.set_page_config(page_title="PLAVE Vote Tracker", page_icon="💙")

st.title("💙 플레이브 투표/시안 업데이트")

# 저장된 파일 읽기
try:
    with open('plave_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    st.caption(f"최근 스캔 결과: 총 {len(data)}개의 정보가 있습니다.")

    for item in data:
        with st.container():
            st.subheader(f"@{item['account']}")
            st.write(item['text'])
            if item['images']:
                st.image(item['images'][0])
            st.markdown(f"[트윗 링크]({item['link']})")
            st.divider()
except FileNotFoundError:
    st.error("데이터 파일이 아직 생성되지 않았습니다. GitHub Actions가 실행될 때까지 기다려주세요.")
