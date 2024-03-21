# 라이브러리 호출
import requests
import json

# # 카카오톡 메시지 API - 리프레쉬 토큰과 액션 토큰 확인
# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "751e98ad2578e3ca32804ce81e927e58", # {REST API}
#     "redirect_url" : "https://localhost:3000",
#     "code" : "NC7H9EVYDnFzQlgtWV-Pf4maLJ8UyM-i8vROX0UGBL-7O1K_-NNYXkGMAIcKPXUZAAABjjpfu00p9hBbJybEWQ" # {CODE}
# }
# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)

# # 카카오톡 메시지 API - 리프레쉬 토큰을 기준으로 액션 토큰 갱신
# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type": "refresh_token",
#     "client_id": "751e98ad2578e3ca32804ce81e927e58",    # {REST API}
#     "refresh_token": "ODmvPhKRHlP1qA1sbBih-mkID0t12WIMFdUKKiVSAAABjjpgvGhV7imzm104lw"   # {CODE}
# }
# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)

# # kakao_code.json 파일 저장
# with open("./resource/kakaoTalkMessage/kakao_code_friend.json", "w") as fp:
#     json.dump(tokens, fp)


# 카카오 API 엑세스 토큰 kakao_code.json 불러오기
with open("./resource/kakaoTalkMessage/kakao_code_friend.json", "r") as fp:
    tokens = json.load(fp)    
# print(tokens)
print(tokens["access_token"])


# 친구 목록 가져오기
url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
result = json.loads(requests.get(url, headers=header).text)
friends_list = result.get("elements")
print(friends_list)

# 친구 목록 중 0번째 리스트의 친구 'uuid'
friend_id = friends_list[0].get("uuid")
print(friend_id)

# 카카오톡 메시지 보내기
def send_message():
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    header = {"Authorization": 'Bearer ' + tokens["access_token"]}
    data={
        'receiver_uuids': '["{}"]'.format(friend_id),
        "template_object": json.dumps({
            "object_type":"text",
            "text":"[LEMMY Test] 응급상황 발생!",
            "link":{
                "web_url" : "https://expc.unist.ac.kr",
                "mobile_web_url" : "https://expc.unist.ac.kr"
            },
            "button_title": "119 호출하기"
        })
    }
    response = requests.post(url, headers=header, data=data)
    response.status_code

if __name__ == "__main__":
    send_message()
    print("Hello World!")  
