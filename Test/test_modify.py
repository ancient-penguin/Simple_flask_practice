import requests
import random

# 테스트할 때마다 새로운 아이디를 만들기 위해 랜덤 숫자 사용
# (이미 있는 아이디면 가입이 안 되니까요!)
rand_id = random.randint(1, 9999)
username = f"tester_{rand_id}"
password = "mypassword"

BASE_URL = "http://127.0.0.1:5000"

print(f"--- 테스트 시작 (ID: {username}) ---")

# [Step 0] 회원가입 (님의 지적대로 이 과정이 필수입니다!)
print("\n=== 1. 회원가입 시도 ===")
register_data = {"username": username, "password": password}
res = requests.post(f"{BASE_URL}/register", json=register_data)
print(f"가입 결과: {res.status_code} (201이면 성공)")

# [Step 1] 로그인 (토큰 받기)
print("\n=== 2. 로그인 및 토큰 발급 ===")
login_data = {"username": username, "password": password}
res = requests.post(f"{BASE_URL}/login", json=login_data)

if res.status_code != 200:
    print("로그인 실패! 테스트를 종료합니다.")
    exit()

token = res.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print("✅ 로그인 성공! 토큰 획득.")

# [Step 2] 메모 작성
print("\n=== 3. 메모 작성 (POST) ===")
create_res = requests.post(f"{BASE_URL}/memo", json={"content": "원본 내용"}, headers=headers)
print(f"작성 결과: {create_res.status_code}")

# 작성한 메모 ID 알아내기 (가장 최근 것)
my_memos = requests.get(f"{BASE_URL}/memo", headers=headers).json()['memos']
target_id = my_memos[-1]['id']
print(f"방금 작성한 메모 번호: {target_id}번")

# [Step 3] 메모 수정
print(f"\n=== 4. {target_id}번 메모 수정 (PUT) ===")
update_res = requests.put(
    f"{BASE_URL}/memo/{target_id}", 
    json={"content": "수정된 내용입니다!"}, 
    headers=headers
)
print(f"수정 상태: {update_res.status_code}")
print(f"수정 내용: {update_res.json()}")

# [Step 4] 메모 삭제
print(f"\n=== 5. {target_id}번 메모 삭제 (DELETE) ===")
delete_res = requests.delete(f"{BASE_URL}/memo/{target_id}", headers=headers)
print(f"삭제 상태: {delete_res.status_code}")

print("\n--- 모든 테스트 완료! ---") 