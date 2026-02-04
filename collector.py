import json
import os
from ntscraper import Nitter

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
    
    # 1. 기존 데이터 불러오기 (중복 체크용)
    file_path = 'plave_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                total_data = json.load(f)
            except:
                total_data = []
    else:
        total_data = []

    # 기존에 저장된 트윗 링크들만 따로 추출 (Set 자료형으로 빠른 비교)
    existing_links = {item['link'] for item in total_data}

    for account in TARGET_ACCOUNTS:
        try:
            tweets = scraper.get_tweets(account, mode='user', number=15)
            for t in tweets['tweets']:
                # 중복 체크: 이미 있는 링크면 건너뜀
                if t['link'] in existing_links:
                    continue
                
                text = t['text']
                # 필터링: PLAVE(대문자) 또는 멤버 이름 포함 여부
                if any(kw in text for kw in ['PLAVE', '예준', '노아', '밤비', '은호', '하민', '투표', '시안']):
                    new_data.append({
                        "account": account,
                        "text": t['text'],
                        "date": t['date'],
                        "link": t['link'],
                        "images": t['pictures']
                    })
        except Exception as e:
            print(f"Error scanning {account}: {e}")
            continue
            
    # 2. 새 데이터와 기존 데이터 합치기
    # 새 데이터를 앞쪽에 배치하여 최신순 유지
    final_data = new_data + total_data
    
    # 3. 데이터 개수 제한 (너무 많아지면 앱이 느려지므로 최신 200개만 유지)
    final_data = final_data[:200]

    # 4. 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"업데이트 완료: 새 트윗 {len(new_data)}개 추가됨.")

if __name__ == "__main__":
    collect()
