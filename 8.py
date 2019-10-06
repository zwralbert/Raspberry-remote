import cv2 as cv
import os
from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 百度人脸识别API账号信息
APP_ID = '17376434'
API_KEY = 'ekQO43AAhRF4Q3Q78SR45sLx'
SECRET_KEY = '2p0s8elDvSK4DdV82gTQs5ghRFVtzeDA'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
# 图像编码方式
IMAGE_TYPE = 'BASE64'
# 用户组信息
GROUP = 'you'
camera = PiCamera()
pygame.mixer.init()
GPIO_IN_PIN = 15
GPIO_IN_PIN1 = 40


# 定义一个摄像头对象
def getimage():
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/faceimage.jpg')
    pygame.mixer.music.load('/home/pi/voice/start.mp3')
    pygame.mixer.music.play()
    time.sleep(2)


# 对图片的格式进行转换
def transimage():

    f = open('/home/pi/faceimage.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img

# 播放声音
def playvioce(name):
    pygame.mixer.music.load('/home/pi/voice/' + name)
    pygame.mixer.music.play()


# 发送信息到微信上
def sendmsg():
    url = "https://sc.ftqq.com/SCU62969T495517f4d64b77824be92edb086f1e285d918a3375e0d.send?"
    urllib.request.urlopen(url +"text=hello,welcome")
# 发送信息到邮箱
def send():
    sender = '359283109@qq.com'
    receivers = '937351848@qq.com'
    password = 'vsbkdarpyirhbhbb'
    message = MIMEMultipart('related')
    subject = '有人来访！'
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')
    message.attach(content)

    file = open("/home/pi/faceimage.jpg", "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    message.attach(img)

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP开启的邮箱和端口，笔者这里是qq邮箱的
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        print ("邮件发送成功！")
    except smtplib.SMTPException:
        print('邮件发送失败！')


# 上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 80:
            print("Welcome %s !" % name)
            if name == 'xxxxxx':
                sendmsg()
                playvioce('xxxxxx.mp3')
                send()
                time.sleep(5)
            if name == 'chenyaxuan':
                sendmsg()
                playvioce('wanggangdan.mp3')
                send()
                print("陈亚玄欢迎你")
                time.sleep(5)

            if name == 'zengweirong':
                sendmsg()
                playvioce('wanggangdan.mp3')
                send()
                print("曾伟荣欢迎你")
                time.sleep(5)
        else:
            print("Sorry...I don't know you !")
            playvioce('noroot.mp3')
            name = 'Unknow'
            return 0
        # 将开门信息存在log.txt文档中
        curren_time = time.asctime(time.localtime(time.time()))
        f = open('Log.txt', 'a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time) + '\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('There is no face in image!')
        playvioce('face.mp3')
        time.sleep(2)
        return 0
    else:
        print(result['error_code'] + ' ' + result['error_code'])
        return 0




# 主函数
if __name__ == '__main__':
    playvioce('waite.mp3')
    time.sleep(3)
    while True:
        time.sleep(0.5)
        print('等待检测')
        getimage()
        time.sleep(0.5)
        img = transimage()
        time.sleep(0.5)
        res = go_api(img)
        print('waite 3 seconds to do next')
        time.sleep(3)