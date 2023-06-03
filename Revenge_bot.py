from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from io import BytesIO
import win32clipboard
from PIL import Image
import random

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()



driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
driver.maximize_window()

# Texts which you want to send
text= "you have made a mistake dear"
text2="  Its time to REPENT ! "

TSK_list = ['tişkler', 'teşe', 'tşk', 'tişk', 'tşe', 'tşi', 'tış', 'tşı','tiskler', 'tese', 'tisk', 'tse', 'tsi', 'tıs', 'tsı']

# Time provided to scan the QR code of Whatsapp Web
time.sleep(40)

# List of names to which you want to send the message
namelist = ["Lina","Loay"]

while(1):
    for name in namelist:
        # Click on the search-bar 
        getsearchbox = driver.find_element(By.XPATH,"//*[@id='side']/div[1]/div/div/div[2]/div/div[1]")
        getsearchbox.click()
        time.sleep(1)

        # Type the name of contactx
        getsearchbox.send_keys(name)
        time.sleep(2)

        # Check if there is any unread message
        unreadMsgs=False
        try:
            getlist=driver.find_element(By.XPATH,"//span[@data-testid='icon-unread-count']")
        except:
            print("no new messages")
            getsearchbox.send_keys(Keys.CONTROL,"a");
            getsearchbox.send_keys(Keys.DELETE);
        else: 
            unreadMsgs=True
            

        
        # If there is no unread message, then click on back in the search bar
        if not unreadMsgs:
            cutit=driver.find_element(By.XPATH,"//*[@id='side']/div[1]/div/div/div[2]/div/div[1]")
            cutit.click()
        
        # If an unread message exists, reply to the contact     
        else:
            # Click on the Chat
            user=driver.find_element(By.XPATH,"//span[@title = '{}']".format(name))
            user.click()

            #Check for teskur

            last_text=driver.find_element(By.XPATH,"(//div[contains(@class,'message-in')])[last()]")

            res = [ele for ele in TSK_list if(ele in last_text.text.lower())]
            if(bool(res)):
                # Type the message on the Chatbox
                textbox=driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")
                textbox.click()
                textbox.send_keys(text)
                textbox.send_keys(name)
                textbox.send_keys(text2)

                imageid = str(int(10*random.random()))



                #filepath = 'reaction1.jpg'
                filepath = 'reaction'+imageid+'.jpg'
                image = Image.open(filepath)

                output = BytesIO()
                image.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]
                output.close()
                send_to_clipboard(win32clipboard.CF_DIB, data)

                textbox.send_keys(Keys.CONTROL,"v");
                time.sleep(2)
                # Send Message
                #send=driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button")
                send=driver.find_element(By.XPATH,"//*[@id='app']/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div")
                send.click()

                getsearchbox.click()
                getsearchbox.send_keys("Reminder")
                user=driver.find_element(By.XPATH,"//span[@title = '{}']".format("Reminder"))
                user.click()



                # Print in contact name in the terminal
                print(name,"texted you!")

            time.sleep(3)
    
    # The code will run again after 300 seconds (5 Minutes)
    time.sleep(2)

driver.quit()