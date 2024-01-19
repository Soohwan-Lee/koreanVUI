# 라이브러리 호출
import requests
import json

# # 카카오톡 메시지 API
# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "7b82d66ab24cd36577acca5e7b46671a",
#     "redirect_url" : "https://localhost:3000",
#     "code" : "Al0_93VEa0H2STnq9Fc3lXkuNEGZA2pSObzhw_t12GJxMRULkm4Xgel2diQKPXWbAAABjSCnQV_E017PSiBv1Q"
# }
# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)
# print("=============")

# # kakao_code.json 파일 저장
# with open("./resource/kakaoTalkMessage/kakao_code.json", "w") as fp:
#     json.dump(tokens, fp)

# kakao_code.json - access token 다시 불러오기
with open("./resource/kakaoTalkMessage/kakao_code.json", "r") as fp:
    tokens = json.load(fp)    
print(tokens["access_token"])

### Text 형태로 작성된 메시지를 보내는 함수
def send_text_form():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }
    data = {
        "template_object" : json.dumps({ "object_type" : "text",
                                        "text" : "[LAMMY Test Message] 현재 응급 상황이 발생하였습니다.",
                                        "link" : {
                                                    "web_url" : "https://expc.unist.ac.kr",
                                                    "mobile_web_url" : "https://expc.unist.ac.kr"
                                                }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

### List 형태로 작성된 메시지
def send_list_form():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }
    template = {
        "object_type" : "list",
        "header_title" : "[LAMMY Test Message]",
        "header_link" : {
            "web_url" : "www.google.com",
            "mobile_web_url" : "www.google.com"
        },
        "contents" : [
            {
                "title" : "1. 낙상 감지 안내",
                "description" : "사용자의 낙상이 감지되었습니다.",
                "image_url" : "https://images.app.goo.gl/vYa4cAhrR3tfn19H6",
                "image_width" : 50, "image_height" : 50,
                "link" : {
                    "web_url" : "https://www.google.co.kr/search?q=national+park&source=lnms&tbm=nws",
                    "mobile_web_url" : "https://www.google.co.kr/search?q=national+park&source=lnms&tbm=nws"
                }
            },
            {
                "title" : "2. 119 호출 제안",
                "description" : "119로 연결해드릴까요?",
                "image_url" : "https://images.app.goo.gl/5Kq4FQMRkTdRVz756",
                "image_width" : 50, "image_height" : 50,
                "link" : {
                    "web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
                    "mobile_web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
                }
            }
        ],
        "buttons" : [
            {
                "title" : "119에 연결",
                "link" : {
                    "web_url" : "www.google.com",
                    "mobile_web_url" : "www.google.com"
                }
            }
        ]
    }
    data = {
        "template_object" : json.dumps(template)
    }
    response = requests.post(url, data=data, headers=headers)
    # print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


if __name__ == "__main__":
#    send_text_form()
   send_list_form()