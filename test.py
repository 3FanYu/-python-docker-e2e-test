import asyncio
from selenium import webdriver
import time 
from urllib.request import urlretrieve
from selenium.webdriver import ActionChains
import base64
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from fpdf import FPDF
import json 
import os
import sys



async def performClick(driver,xpath):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element=driver.find_element_by_xpath(xpath)
    element.click()

async def performWrite(driver,xpath,inputs):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    element=driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(inputs)

async def downloadImage(driver,xpath,fileName):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    img = driver.find_element_by_xpath(xpath)# 找圖片
    src = img.get_attribute('src')
    formattedFileName=fileName+nowForFile+".png"
    urlretrieve(src, formattedFileName) # 下載圖片

def getEnrollData():
    with open('info.json') as f:
        data = json.load(f)
    return data['name'],data['email'],data['tel']

async def beHuman(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scroll(0, 0);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("...I'M HUMAN...")

def writeIntoPDF(thePDF,message,img):
    thePDF.add_page()
    thePDF.text(10,thePDF.get_y(),txt=message)
    thePDF.image(img,0,thePDF.get_y()+5,w=205)

def makedirs():
    if not (os.path.exists('stepOne')):
        os.makedirs('stepOne')
    if not (os.path.exists('stepTwo')):
        os.makedirs('stepTwo')
    if not (os.path.exists('stepThree')):
        os.makedirs('stepThree')
    if not (os.path.exists('ending')):
        os.makedirs('ending')
    if not (os.path.exists('eventImage')):
        os.makedirs('eventImage')
    if not (os.path.exists('Ticket')):
        os.makedirs('Ticket')
    if not (os.path.exists('PDF')):
        os.makedirs('PDF')

def getEnrollDataFromInput():
    name=sys.argv[1] if len(sys.argv)>1 else '測試樊'
    email=sys.argv[2] if len(sys.argv)>2 else 'fanfan9453@gmail.com'
    tel=sys.argv[3] if len(sys.argv)>3 else '0912345678'
    print('...接收輸入資料:...\n ...姓名:'+name+'...\n ...信箱:'+email+'...\n ...電話:'+tel+'...')
    return name,email,tel

name,email,tel=getEnrollDataFromInput()
makedirs()
loop = asyncio.get_event_loop()
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
nowForFile = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
url = 'https://kktix.com/events.json?search=0xFE'
resp = requests.get(url=url)
data = resp.json() # Check the JSON Response Content documentation below
# print("url from api"+data['entry'][0]['url'])
print('...新建pdf文件...')
pdf = FPDF()
pdf.add_font('setofont','','setofont.ttf',True)
pdf.set_font('setofont',size=12)
print('...設定web driver...')
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  #規避google
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
# driver = webdriver.Chrome('/usr/local/bin/chromedriver')

result=driver.get(data['entry'][0]['url'])

loop.run_until_complete(downloadImage(driver,'/html/body/div[2]/div[2]/div/div[3]/img','eventImage/eventImage_'))
# 找標題＆內文
title = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div/h1')
content = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/p[1]')
print("標題:"+title.get_attribute('innerHTML'))
print("內文:\n"+content.get_attribute('innerHTML'))
# 找data-code 
dataCode=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/pre')
dataCodeFormatted=dataCode.get_attribute('innerHTML')[17:33] #裁切字串
decodedDataCode = base64.b64decode(dataCodeFormatted).decode('utf-8') #解碼
# print(decodedDataCode)

screenShot='stepOne/step_one_'+nowForFile+'.png'
driver.save_screenshot(screenShot)
writeIntoPDF(pdf,'步驟一：',screenShot)
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'/html/body/div[2]/div[2]/div/div[7]/a'))
print('...下一步...')
# print(driver.current_url)
#  等待modal載入
loop.run_until_complete(performClick(driver,'//*[@id="guestModal"]/div[2]/div/div[3]/button'))
print('...關閉modal...')
loop.run_until_complete(performClick(driver,'//*[@id="ticket_344407"]/div/span[3]/button[2]'))
print('...票數＋1...')
loop.run_until_complete(performClick(driver,'//*[@id="person_agree_terms"]'))
print('...已閱讀並同意...')

screenShot='stepTwo/step_two_'+nowForFile+'.png'
driver.save_screenshot(screenShot)
writeIntoPDF(pdf,'步驟二：',screenShot)
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button'))
print('...下一頁...')
loop.run_until_complete(performClick(driver,'//*[@id="guestModal"]/div[2]/div/div[3]/button'))
print('...關閉modal...')

loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701843"]/div/div/input',name+now))
print('...寫入姓名:'+name+now+'...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_email_701844"]/div/div/input',email))
print('...寫入信箱:'+email+'...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701845"]/div/div/input',tel))
print('...寫入電話:'+tel+'...')
loop.run_until_complete(performWrite(driver,'//*[@id="field_text_701846"]/div/div/input',decodedDataCode))
print('...寫入data-code...')
loop.run_until_complete(performClick(driver,'//*[@id="person_agree_terms"]'))
print('...我已經閱讀並同意...')

screenShot='stepThree/step_three_'+nowForFile+'.png'
driver.save_screenshot(screenShot)
writeIntoPDF(pdf,'步驟三：',screenShot)
print('...Say Cheese!...')
loop.run_until_complete(beHuman(driver))

loop.run_until_complete(performClick(driver,'//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a'))
print('...確認表單資料...')
loop.run_until_complete(downloadImage(driver,'//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[2]/div/ul/li/div/div/div[1]/div[2]/img','Ticket/event_qr_code_'))
print('...下載活動票券...')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
screenShot='ending/ending_'+nowForFile+'.png'
driver.save_screenshot(screenShot)
writeIntoPDF(pdf,'訂票結果',screenShot)
print('...Say Cheese!...')
print('...取消訂單...')
loop.run_until_complete(performClick(driver,'//*[@id="registrations_controller"]/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/a'))
loop.run_until_complete(performClick(driver,'//*[@id="registrationsShowApp"]/div[2]/div/div/div/div[2]/div/a[1]'))
obj = driver.switch_to.alert
msg=obj.text
print ("...Alert Text: "+ msg+"..." )
obj.accept()
print("...確定...")

print('...完成所有程序，即將關閉瀏覽器...')
driver.quit()#關閉瀏覽器 
pdf.output('PDF/result'+nowForFile+'.pdf', 'F')
