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
text= "You have made a mistake dear "
text2="\nIts time to REPENT ! "

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

whiteList = "abdulrahman albaroudi"
blackList = ["Lına barodi Türkçe", "+90 535 493 91 20"]
keyWords = ['tişkler', 'teşe', 'tşk', 'tişk', 'tşe', 'tşi', 'tış', 'tşı','tiskler', 'tese', 'tisk', 'tse', 'tsi', 'tıs', 'tsı']

while(1):
    # get recent chats
    latestChats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div[1]/div/div/div")
    annoyingFriend = None

    # detect if your annoying friend texted you
    for element in latestChats:
        name = element.find_element(By.XPATH, "./div/div/div/div[2]/div[1]/div[1]/span").text
        print("name = {}".format(name))

        if name in blackList :
            # Check if there is any unread message
            newMsgExist = False
            newMessagesCount = 0
            try:
                number = element.find_element(By.XPATH,"./div/div/div/div[2]/div[2]/div[2]/span[1]/div/span").text
                print("number = {}".format(number))
                newMessagesCount = int(number)
            except:
                print("no new messages")
            else: 
                newMsgExist=True

            if newMsgExist : 
                annoyingFriend = dict(e=element, n=name, c=newMessagesCount)
                break

    if annoyingFriend is not None:
        print("ANNOYING FRIEND DETECTED")
        print(annoyingFriend["n"])
        annoyingFriend["e"].click()

        time.sleep(10)
        # get unread messages
        messages = driver.find_elements(By.XPATH, "//div[contains(@data-testid,'msg-container')]")
        print(annoyingFriend['c'])
        newMessages = messages[-annoyingFriend['c']:]
        for m in newMessages:
            message = m.find_element(By.XPATH, "./div[1]/div[1]/div[1]/div/span[1]/span").text
            print(message)

            # detect if the message contains a keyword
            if message in keyWords:
                print("ANNOYING MESSAGE DETECTED '{}'".format(message))

                # send response
                textBox = driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")
                textBox.click()
                textBox.send_keys(text)
                textBox.send_keys(annoyingFriend["n"])
                textBox.send_keys(text2)
                # pick arandom image
                imageid = str(int(10*random.random()))
                filepath = 'reaction'+imageid+'.jpg'
                image = Image.open(filepath)
                output = BytesIO()
                image.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]
                output.close()
                send_to_clipboard(win32clipboard.CF_DIB, data)
                textBox.send_keys(Keys.CONTROL,"v")
                time.sleep(2)
                sendButton = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH,"//*[@data-testid='send']"))
                assert loggedInPage.is_displayed
                sendButton.click()
                time.sleep(6)
                break

    # driver.find_element(By.XPATH, "//*[@data-testid='search']").click()
    # driver.find_element(By.XPATH,"//*[@id='side']/div[1]/div/div/div[2]/div/div[1]").send_keys(whiteList)
    # driver.find_element(By.XPATH,"(//[@id='pane-side']/div[1]/div/div/)[last()]").click()
    

# close chrome driver
driver.close()  
driver.quit()
