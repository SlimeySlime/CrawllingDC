from bs4 import BeautifulSoup
import requests
import urllib.request
import os  
import re 
import time

start_time = time.time()

jung = "https://gall.dcinside.com/mgallery/board/lists/?id=aoegame" # 중갤
any_euro = "https://gall.dcinside.com/mgallery/board/lists/?id=euca&page=1" # 애니 유럽
baseball = "https://gall.dcinside.com/board/view/?id=baseball_new7&no=15372622&page=1" # 야갤
test = "https://gall.dcinside.com/mgallery/board/lists?id=singlebungle1472" # 테스트용
toon = "https://toonkor.live/%EC%9D%BC%EC%83%81%EC%83%9D%ED%99%9C_%EA%B0%80%EB%8A%A5%ED%95%98%EC%84%B8%EC%9A%94%EF%BC%9F_1%ED%99%94.html"

header = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    # X-Requested-With: XMLHttpRequest
    # Accept-Encoding: gzip, deflate, br
    # Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    # Connection: keep-alive
    # Cookie: PHPSESSID=861622c428327089fe23f00fc664bb75; ci_c=772b7d56b83d2f9b477e45710ca2a53d; __utma=118540316.606081115.1557500972.1557500972.1557500972.1; __utmc=118540316; __utmz=118540316.1557500972.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.2.606081115.1557500972; _gid=GA1.2.754843687.1557500972; alarm_popup=1; last_alarm=1557500998; ck_lately_gall=6qv%7C1Ol; gallRecom=MjAxOS0wNS0xMSAwMDoxMDoyMS9jZjIyODY1Yjc0ODhjNmQ1ODYwZGFjNjMwYzRlNjFhYzE4Mjk1ODdkZWE0ZjQxMDg4NzAxOTkzNzEwYjdhMWIy; service_code=21ac6d96ad152e8f15a05b7350a2475909d19bcedeba9d4face8115e9bc2fa4d579966ba0ccb263b15c97b870e4dae7ff6a98ad2fb0a4e827afae0e9a08f8d372e3c40c5f101004b5d68096f9a5068d59d769f26b34f583f7ec699422966436489e8d3bda6ae7475414f41ef647e2ed1b8203b9597d299bcc8717c3d387fea666da9c9d06e2c5655c2ca56cc1c3c794bb1205f3eaa56fe0874caf2f2ce85c8af4f3ef9b769086fcb6d2e799e1c6a7a2fedee126354a49e93c6ce5f83a6f2d8ee848bf33b03a63c84901d5e812fa190ea; wcs_bt=f92eaecbc22aac:1557501024; __utmb=118540316.8.10.1557500972
    # Host: gall.dcinside.com
    # Referer: https://gall.dcinside.com/mgallery/board/lists?id=singlebungle1472
}

# 갤러리 선택
folder = "./Jung"
response = requests.get(jung, headers = header) # 리퀘스트 시작 , 주소와 헤더를 넣어서 리퀘스트
soup = BeautifulSoup(response.text,"html.parser")   # 리스폰스 파싱 바로 soup로
req = urllib.request
# print(response.text)
# print(soup)

toList = []
originFolderList = os.listdir(folder)
for origins in originFolderList:
    toList.append(str(re.findall('\d+',origins)[0])) # toList = 다운로드 폴더의 이미지 리스트 

# for i in soup.find_all("div",{"class":"view-wrap"}):
#     f = open(folder+".txt",'w')
#     f.write(str(i))
#     print(i)
    
def dcCrwal():
    # 따라하기
    print(soup)
    for i in soup.find_all("td","gall_tit ub-word"):
        poops = i.find("a")
        print(i)
        # poops는 <a href="/mgallery/board/view/?id=aoegame&amp;no=7195048&amp;page=1">
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
                    html = requests.get(url)
                    # 수프로 본문 img태그에 src를 가져옴 
                    link2 = BeautifulSoup(html.text,"html.parser")
                    bonmun = link2.find("div",{"class":"writing_view_box"})
                    imageLink = bonmun.find("img").get("src")
                    # 그 소스의 true이미지링크 값을 가져옴
                    replaceA = "dcimg6.dcinside.co.kr/viewimage"
                    replaceB = "image.dcinside.com/viewimage"
                    trueImageLink = imageLink.replace(replaceA,replaceB)

                    # 파일 쓰기 단계
                    # a = req.urlopen(trueImageLink) # 이미지 url오픈
                    r = requests.get(trueImageLink)
                    with open(folder + "/" + WritingNum + ".png","wb") as f:
                        # f.write(a.read()) 
                        f.write(r.content)
                except Exception as e:
                    print (WritingNum + " 도중 문제발생 \n 에러 : ")
            
dcCrwal()           

end_time = time.time()
print("걸린시간 = " + str(end_time - start_time) + "초" )
        


    
    