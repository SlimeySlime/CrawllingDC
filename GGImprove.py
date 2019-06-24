from bs4 import BeautifulSoup
import sys, argparse
import requests, urllib.request
import os  
import re 
import time
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

start_time = time.time()

jung = "https://gall.dcinside.com/mgallery/board/lists?id=aoegame" # 중갤
any_euro = "https://gall.dcinside.com/mgallery/board/lists/?id=euca&page=1" # 애니 유럽
baseball = "https://gall.dcinside.com/board/lists/?id=baseball_new8" # 야갤
test = "https://gall.dcinside.com/board/lists/?id=america_ani" # 테스트용 애미갤
toon = "https://toonkor.live/%EC%9D%BC%EC%83%81%EC%83%9D%ED%99%9C_%EA%B0%80%EB%8A%A5%ED%95%98%EC%84%B8%EC%9A%94%EF%BC%9F_1%ED%99%94.html"

header = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

# 갤러리 선택
folder = "./any_euro"   # 폴더변경 
response = requests.get(any_euro,headers=header) # 리퀘스트 시작 주소변경, 헤더넣기
soup = BeautifulSoup(response.text,"html.parser")
req = urllib.request

toList = []
originFolderList = os.listdir(folder)
for origins in originFolderList:
    toList.append(str(re.findall('\d+',origins)[0])) # toList = 다운로드 폴더 

# for i in soup.find_all("div",)
#     print(i)
    

def dcCrwal():
    # 따라하기
    for i in soup.find_all("td","gall_tit ub-word"):
        poops = i.find("a")         # poops는 <a href="/mgallery/board/view/?id=aoegame&amp;no=7195048&amp;page=1">
                                    # <em class="icon_img icon_pic"></em>데이빗 핫셀호프는 뭔데 갑자기 뜸</a> 이러한 내용을 담고있음
        WritingNum = re.findall("\d+",str(poops))[0] # 게시글 넘버 따오기
        if toList.__contains__(WritingNum):
            print ("이미 있는 파일입니다.")
        else:
            if (str(poops).find("icon_pic")) != -1:
                print(WritingNum + ".png 파일을 다운로드하고있습니다.")

                try:
                    # 본문에 있는 href 태그로 리퀘스트를 날림
                    url = "https://gall.dcinside.com" + str(poops.get("href"))
                    html = requests.get(url,headers=header)
                    # 수프로 본문 img태그에 src를 가져옴 
                    link2 = BeautifulSoup(html.text,"html.parser")
                    bonmun = link2.find("div",{"class":"writing_view_box"})
                    imageLink = bonmun.find("img").get("src")
                    # 그 소스의 true이미지링크 값을 가져옴
                    replaceA = "dcimg6.dcinside.co.kr/viewimage"
                    replaceB = "image.dcinside.com/viewimage"
                    trueImageLink = imageLink.replace(replaceA,replaceB)

                    # 파일 쓰기 단계
                    a = req.urlopen(trueImageLink) # 이미지 url오픈
                    f = open(folder + "/" + WritingNum + ".png","wb") 
                    f.write(a.read()) 
                except Exception as e:
                    print (WritingNum + " 도중 문제발생 \n 에러 : ")
              
if __name__ == "__main__":
    dcCrwal()

end_time = time.time()
print("걸린시간 = " + str(end_time - start_time) + "초" )
        
