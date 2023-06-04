from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from io import BytesIO
from PIL import Image
import win32clipboard
import random
import time

# open chrome webdriver on whatsapp web
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)  
driver.get("https://web.whatsapp.com/")  

# wait until QR code is scanned and whatsapp web is connected
loggedInPage = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH, "//*[@id='app']/div/div/div[4]/header/div[1]/div/img"))
assert loggedInPage.is_displayed

# Texts which you want to send
text= "you have made a mistake dear"
text2="  Its time to REPENT ! "

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

BlackList = ["abdulrahman albaroudi", "Lına barodi Türkçe"]
keyWords = ['tişkler', 'teşe', 'tşk', 'tişk', 'tşe', 'tşi', 'tış', 'tşı','tiskler', 'tese', 'tisk', 'tse', 'tsi', 'tıs', 'tsı']

while(1):
    # get recent chats
    latestChats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div[1]/div/div/div")
    annoyingFriend = None

    # detect if your annoying friend texted you
    for element in latestChats:
        name = element.find_element(By.XPATH, "./div/div/div/div[2]/div[1]/div[1]/span").text
        # isNotRead = element.find_element(By.XPATH, "./div/div/div/div[2]/div[2]/div[2]/span[1]/div").is_displayed
        if name in BlackList : #and isNotRead:
            annoyingFriend = dict(e=element, n=name )
            break

    if annoyingFriend is not None:
        print("ANNOYING FRIEND DETECTED")
        print(annoyingFriend["n"])
        annoyingFriend["e"].click()

        # get unread messages
        messages = driver.find_elements(By.XPATH, "//*[@id='main']/div[2]/div/div[2]/div[3]")
        for m in messages:
            if m.get_attribute("class") != "row" : 
                messages.remove(m)
                break
            messages.remove(m)

        # detect if the message contains a keyword
        for m in messages:
            message = m.find_element(By.XPATH, "//*[@id='main']/div[2]/div/div[2]/div[3]/div[10]/div/div/div/div[1]/div[1]/div[1]/div/span[1]/span").text
            if message in keyWords:
                print("ANNOYING MESSAGE DETECTED")
                print(message)
                # send response
                textBox=driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")
                textBox.click()
                textBox.send_keys(text)
                textBox.send_keys(annoyingFriend["n"])
                textBox.send_keys(text2)
                imageid = str(int(10*random.random()))
                filepath = 'reaction'+imageid+'.jpg'
                image = Image.open(filepath)
                output = BytesIO()
                image.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]
                output.close()
                send_to_clipboard(win32clipboard.CF_DIB, data)
                textBox.send_keys(Keys.CONTROL,"v")
                sendButton = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH,"//*[@id='app']/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div"))
                assert loggedInPage.is_displayed
                sendButton.click()
                break
        # close chat
        driver.find_element(By.XPATH, "//*[@id='pane-side']/div[1]/div/div/div/div[2]").click()

# close chrome driver
driver.close()  
driver.quit()
