import json
import os
from ntscraper import Nitter
from datetime import datetime

# 1. 계정 성격에 따라 두 그룹으로 분류
# A그룹: 플레이브 관련 정보만 주로 올라오는 계정 (키워드 검사 없이 수집)
PLLI_FAVORITE_ACCOUNTS = [
    "picnic_kr", "giftreeofficial", "lovedol_vote", "HIGHER_twt"
]

# B그룹: 여러 아이돌이 섞여 있는 대형 투표 앱 (반드시 키워드 검사 필요)
GENERAL_VOTE_ACCOUNTS = [
    "starnewskorea", "sda_official", "GoldenDisc", "fanplus_app", "thefactnews", 
    "myloveidol_kpop", "MubeatOfficial", "bigc_kr", "twt_my1pick", "podoal_official", 
    "genie_kt", "melon", "bugs_official_", "idolchamp1", "UPICK_twt", "duckad2020",
    "idoki_twt", "Whosfan_Ofcl", "idolpick_vote", "linc_fan", "kooky__official",
    "muniverse_io", "celeb_champ", "STARDOM_twt"
]

def collect():
    scraper = Nitter()
    new_data = []
    file_path = 'plave_data.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try: total_data = json.load(f)
            except: total_data = []
    else:
        total_data = []

    existing_links = {item['link'] for item in total_data}

    # 플레이브 전용 키워드
    plave_keywords = [
        'PLAVE', '플레이브', 'PLLI', '플리',
        '예준', 'YEJUN', '노아', 'NOAH', '밤비', 'BAMBI', '은호', 'EUNHO', '하민', 'HAMIN'
    ]

    # 모든 계정 리스트 합치기
    all_accounts = [(acc, "A") for acc in PLLI_FAVORITE_ACCOUNTS] + [(acc, "B") for acc in GENERAL_VOTE_ACCOUNTS]

    for account, group_type in all_accounts:
        try:
            print(f"@{account} 스캔 중...")
            tweets = scraper.get_tweets(account, mode='user', number=40)
            
            for t in tweets['tweets']:
                if t['link'] in existing_links: continue
                
                text = t['text']
                is_target = False
                
                # A그룹은 무조건 수집, B그룹은 키워드가 있을 때만 수집
                if group_type == "A":
                    is_target = True
                else:
                    if any(kw.upper() in text.upper() for kw in plave_keywords):
                        is_target = True
                
                if is_target:
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
            
    final_data = new_data + total_data
    final_data = final_data[:300]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"업데이트 완료: 새 소식 {len(new_data)}개 추가.")

if __name__ == "__main__":
    collect()
