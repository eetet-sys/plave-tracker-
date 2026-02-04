import json
import os
from ntscraper import Nitter
from datetime import datetime

# 계정 분류
PLLI_FAVORITE_ACCOUNTS = ["picnic_kr", "giftreeofficial", "lovedol_vote", "HIGHER_twt"]
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

    # 확장된 키워드 세트 (투표 단어 미포함 시 대비)
    plave_names = ['PLAVE', '플레이브', 'PLLI', '플리', '예준', 'YEJUN', '노아', 'NOAH', '밤비', 'BAMBI', '은호', 'EUNHO', '하민', 'HAMIN']
    action_keywords = ['시안', 'DESIGN', '광고', 'AD', 'SUPPORT', '순위', 'RANK', '결과', 'RESULT', '참여', 'JOIN', 'EVENT']
    account_ids = PLLI_FAVORITE_ACCOUNTS + GENERAL_VOTE_ACCOUNTS
    
    search_keywords = [kw.upper() for kw in (plave_names + action_keywords + account_ids)]

    all_accounts = [(acc, "A") for acc in PLLI_FAVORITE_ACCOUNTS] + [(acc, "B") for acc in GENERAL_VOTE_ACCOUNTS]

    for account, group_type in all_accounts:
        try:
            print(f"@{account} 스캔 중...")
            tweets = scraper.get_tweets(account, mode='user', number=50)
            
            for t in tweets['tweets']:
                if t['link'] in existing_links: continue
                
                text = t['text'].upper()
                is_target = False
                
                # A그룹(플리 전용)은 무조건, B그룹은 확장 키워드 매칭 시 수집
                if group_type == "A":
                    is_target = True
                else:
                    if any(kw in text for kw in search_keywords):
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
    print(f"완료: {len(new_data)}개 추가.")

if __name__ == "__main__":
    collect()
