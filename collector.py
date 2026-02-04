import json
import os
from ntscraper import Nitter
from datetime import datetime

# 1. 주시할 계정 리스트 (28개)
TARGET_ACCOUNTS = [
    "picnic_kr", "giftreeofficial", "lovedol_vote", "starnewskorea", "sda_official",
    "HIGHER_twt", "GoldenDisc", "fanplus_app", "thefactnews", "myloveidol_kpop",
    "MubeatOfficial", "bigc_kr", "twt_my1pick", "podoal_official", "genie_kt",
    "melon", "bugs_official_", "idolchamp1", "UPICK_twt", "duckad2020",
    "idoki_twt", "Whosfan_Ofcl", "idolpick_vote", "linc_fan", "kooky__official",
    "muniverse_io", "celeb_champ", "STARDOM_twt"
]

def collect():
    scraper = Nitter()
    new_data = []
    file_path = 'plave_data.json'
    
    # 기존 데이터 로드 (중복 제거용)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                total_data = json.load(f)
            except:
                total_data = []
    else:
        total_data = []

    existing_links = {item['link'] for item in total_data}

    # 수집 키워드 (한글 + 영문 활동명)
    keywords = [
        'PLAVE', '플레이브',
        '예준', 'Yejun', 'YEJUN',
        '노아', 'Noah', 'NOAH',
        '뱀비', 'Bambi', 'BAMBI',
        '은호', 'Eunho', 'EUNHO',
        '하민', 'Hamin', 'HAMIN',
        '투표', 'VOTE', 'vote',
        '시안', 'DESIGN', 'design'
    ]

    for account in TARGET_ACCOUNTS:
        try:
            print(f"@{account} 스캔 중...")
            # 1월 소식까지 훑기 위해 수집 개수를 50개로 설정
            tweets = scraper.get_tweets(account, mode='user', number=50)
            
            for t in tweets['tweets']:
                if t['link'] in existing_links:
                    continue
                
                text = t['text']
                # 키워드 필터링 (대문자 PLAVE 포함)
                if any(kw in text for kw in keywords):
                    # 날짜 체크 (1월, 2월 데이터 위주로 수집)
                    tweet_date = t['date']
                    if "Jan" in tweet_date or "Feb" in tweet_date:
                        new_data.append({
                            "account": account,
                            "text": t['text'],
                            "date": t['date'],
                            "link": t['link'],
                            "images": t['pictures']
                        })
        except Exception as e:
            print(f"Error at @{account}: {e}")
            continue
            
    # 새 데이터 + 기존 데이터 합치기 (최신 300개 유지)
    final_data = new_data + total_data
    final_data = final_data[:300]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"성공! 새 소식 {len(new_data)}개가 추가되었습니다.")

if __name__ == "__main__":
    collect()
