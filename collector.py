import json
import os
from ntscraper import Nitter
from datetime import datetime
import time

# 계정 리스트
PLLI_FAVORITE_ACCOUNTS = ["picnic_kr", "giftreeofficial", "lovedol_vote", "HIGHER_twt"]
GENERAL_VOTE_ACCOUNTS = [
    "starnewskorea", "sda_official", "GoldenDisc", "fanplus_app", "thefactnews", 
    "myloveidol_kpop", "MubeatOfficial", "bigc_kr", "twt_my1pick", "podoal_official", 
    "genie_kt", "melon", "bugs_official_", "idolchamp1", "UPICK_twt", "duckad2020",
    "idoki_twt", "Whosfan_Ofcl", "idolpick_vote", "linc_fan", "kooky__official",
    "muniverse_io", "celeb_champ", "STARDOM_twt"
]

def collect():
    # [변경] 인스턴스 체크를 건너뛰고 더 안정적인 서버 접속 시도
    scraper = Nitter(log_level=1, skip_instance_check=False)
    new_data = []
    file_path = 'plave_data.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try: total_data = json.load(f)
            except: total_data = []
    else:
        total_data = []

    existing_links = {item['link'] for item in total_data}
    search_keywords = ['PLAVE', '플레이브', 'PLLI', '플리', '예준', '노아', '밤비', '은호', '하민', 'VOTE', '투표', '시안']

    all_accounts = [(acc, "A") for acc in PLLI_FAVORITE_ACCOUNTS] + [(acc, "B") for acc in GENERAL_VOTE_ACCOUNTS]

    for account, group_type in all_accounts:
        try:
            print(f"@{account} 스캔 중...")
            # [변경] 1월 소식까지 긁기 위해 수집 개수를 80개로 늘림
            tweets = scraper.get_tweets(account, mode='user', number=80)
            
            if not tweets.get('tweets'):
                print(f"@{account}: 응답 없음, 다음 계정으로 이동")
                continue

            for t in tweets['tweets']:
                if t['link'] in existing_links: continue
                
                text = t['text'].upper()
                is_target = (group_type == "A") or any(kw.upper() in text for kw in search_keywords)
                
                if is_target:
                    # 2026년 데이터라면 일단 모두 수집
                    if "2026" in t.get('date', ''):
                        new_data.append({
                            "account": account,
                            "text": t['text'],
                            "date": t['date'],
                            "link": t['link'],
                            "images": t['pictures']
                        })
            
            # 서버 과부하 방지를 위해 잠시 쉬기
            time.sleep(1)
            
        except Exception as e:
            print(f"@{account} 에러: {e}")
            continue
            
    # 최종 저장 (이제 권한이 있으므로 이 부분이 실행됩니다)
    final_data = new_data + total_data
    final_data = final_data[:400]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"성공! 새 소식 {len(new_data)}개를 파일에 저장했습니다.")

if __name__ == "__main__":
    collect()
