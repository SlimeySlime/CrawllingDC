import sys
import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
MYAPP_KEY = '6b9e85f7c70e6e7d71eec8a8162ee946'

def detect_adult(image_url):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        # data = { 'file' : open('7237817.png', 'rb')}        # image_url이 아닌 file 형태로 시도
        data = { 'image_url' : image_url}
        resp = requests.post(API_URL, headers=headers, data=data)   # response(resp)는 API_URL에 헤더와 데이터를 넣은 리턴값 
        resp.raise_for_status()     # 내부는 아무도 모를 raise_for_status() 와 그 result 
        result = resp.json()['result']
        print("성인확률 : " + str(result['adult']))
        print("노출확률 : " + str(result['soft']))
        print("평범확률 : " + str(result['normal']))
        if result['adult'] > result['normal'] and result['adult'] > result['soft']:
            print("성인 이미지일 확률이 {}% 입니다.".format(result['adult']*100))
        elif result['soft'] > result['normal'] and result['soft'] > result['adult']:
            print("노출이 포함된 이미지일 확률이 {}% 입니다.".format(result['soft']*100))
        else :
            print("일반적인 이미지일 확률이 {}% 입니다.".format(result['normal']*100))

    except Exception as e:
        print(str(e))
        sys.exit(0)

imgurl = "https://i.stack.imgur.com/Y48mb.png"
detect_adult(imgurl)

# __main__말고 이렇게 호출만 해도 작동하긴함 /// 하지만 문제는 url이 아니라 file을 매개변수로 주도록 바꿔야하는데...

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Classify adult image.')
#     parser.add_argument('image_url', type=str, nargs='?',
#         default="http://t1.daumcdn.net/alvolo/_vision/openapi/r2/images/10.jpg",
#         # default="https://i.stack.imgur.com/Y48mb.png",
#         help='image url to classify')   # 위의 argparse parser를 이해하고온다

#     args = parser.parse_args()
#     detect_adult(args.image_url)