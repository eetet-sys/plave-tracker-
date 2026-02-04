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

    # 키워드 설정
    plave_names = ['PLAVE', '플레이브', 'PLLI', '플리', '예준', 'YEJUN', '노아', 'NOAH', '밤비', 'BAMBI', '은호', 'EUNHO', '하민', 'HAMIN']
    action_keywords = ['시안', 'DESIGN', '광고', 'AD', 'SUPPORT', '순위', 'RANK', '결과', 'RESULT', '참여', 'JOIN', 'EVENT', 'VOTE', '투표']
    search_keywords = [kw.upper() for kw in (plave_names + action_keywords + PLLI_FAVORITE_ACCOUNTS + GENERAL_VOTE_ACCOUNTS)]

    all_accounts = [(acc, "A") for acc in PLLI_FAVORITE_ACCOUNTS] + [(acc, "B") for acc in GENERAL_VOTE_ACCOUNTS]

    for account, group_type in all_accounts:
        try:
            print(f"--- @{account} 스캔 시작 ---")
            tweets = scraper.get_tweets(account, mode='user', number=50)
            
            # 수집된 트윗이 아예 없는 경우 체크
            if not tweets.get('tweets'):
                print(f"@{account}: 가져온 트윗이 없습니다.")
                continue

            for t in tweets['tweets']:
                if t['link'] in existing_links: continue
                
                text = t['text'].upper()
                is_target = False
                
                if group_type == "A":
                    is_target = True
                else:
                    if any(kw in text for kw in search_keywords):
                        is_target = True
                
                if is_target:
                    # [수정] 날짜 필터를 더 넓게: 2026년 게시글이면 일단 다 가져옴
                    tweet_date = t.get('date', '')
                    if "2026" in tweet_date:
                        new_data.append({
                            "account": account,
                            "text": t['text'],
                            "date": t['date'],
                            "link": t['link'],
                            "images": t['pictures']
                        })
            print(f"@{account}: 현재까지 {len(new_data)}개 발견")
        except Exception as e:
            print(f"@{account} 에러 발생: {e}")
            continue
            
    # 새 데이터 합치기
    final_data = new_data + total_data
    final_data = final_data[:300]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"== 최종 수집 완료: 총 {len(new_data)}개의 새 소식 저장됨 ==")

if __name__ == "__main__":
    collect()
