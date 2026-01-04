import requests
import random

BASE_URL = "http://localhost:5000"

# 해커와 피해자 2개의 아이디 생성. 
# 매번 랜덤 아이디 생성
victim_id = f"user_{random.randint(1,9999)}"
thief_id = f"hacker_{random.randint(1,9999)}"
pw = "password"

def get_token(username):
    requests.post(f"{BASE_URL}/register", json={"username": username, "password": pw})
    res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": pw})
    return res.json()['access_token']

print("--- 해커 테스트 시작 ---")

# 1. 피해자(Victim)가 메모를 하나 작성함
victim_token = get_token(victim_id)
victim_headers = {'Authorization': f'Bearer {victim_token}'}
res = requests.post(f"{BASE_URL}/memo", json={"content": "중요한 비밀 메모"}, headers=victim_headers)

# 피해자의 메모 번호를 알아냄 (가장 마지막 글)
memo_list = requests.get(f"{BASE_URL}/memo", headers=victim_headers).json()['memos']
target_memo_id = memo_list[-1]['id']
print(f"타겟 메모 ID: {target_memo_id} (작성자: {victim_id})")


# --- 테스트 케이스 시작 ---

# Case 1: 토큰 없이 메모 작성 시도 (401 기대)
print("\n[Case 1] 토큰 없이 메모 작성 시도")
res = requests.post(f"{BASE_URL}/memo", json={"content": "도둑질"})
if res.status_code == 401:
    print("✅ 방어 성공! (401 Unauthorized)")
else:
    print(f"❌ 뚫렸음! 상태 코드: {res.status_code}")


# Case 2: 남의 글 수정 시도 (403 기대)
print(f"\n[Case 2] 해커({thief_id})가 피해자({victim_id})의 글 수정 시도")
thief_token = get_token(thief_id) # 해커가 로그인
thief_headers = {'Authorization': f'Bearer {thief_token}'}

res = requests.put(
    f"{BASE_URL}/memo/{target_memo_id}", 
    json={"content": "메모는 내가 해킹했다 킬킬"}, 
    headers=thief_headers
)

if res.status_code == 403:
    print("✅ 방어 성공! (403 Forbidden - 권한 없음)")
else:
    print(f"❌ 뚫렸음! 상태 코드: {res.status_code}")


# Case 3: 없는 메모 조회 시도 (404 기대)
print("\n[Case 3] 존재하지 않는 메모(99999번) 수정 시도")
res = requests.put(
    f"{BASE_URL}/memo/99999", 
    json={"content": "허공에 삽질"}, 
    headers=victim_headers
)

if res.status_code == 404:
    print("✅ 방어 성공! (404 Not Found)")
else:
    print(f"❌ 실패! 상태 코드: {res.status_code}")

print("\n--- 테스트 종료 ---")