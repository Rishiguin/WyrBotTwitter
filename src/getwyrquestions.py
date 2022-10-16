from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from image_edit import FormWyr
import sqlite3
import datetime
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.binary_location =os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()


def get_ques():
    driver.get('https://either.io/')
    a2 = driver.find_elements(By.CLASS_NAME, 'option-text')
    for l in a2:
        print(l.get_attribute('textContent'))
    a = a2[0].get_attribute('textContent')
    b = a2[1].get_attribute('textContent')

    uid = a.lower().strip()+b.lower().strip()

    print('get_ques() : ',[a, b, uid])
    return ([a, b, uid])


# a1=FormWyr().get_image(a=a,b=b)
today = datetime.date.today()
date = '{}'.format([today.year, today.month, today.day])

def get_unique_ques():
    conn = sqlite3.connect('wyr_either.db')
    c = conn.cursor()
    k=0
    try:
        while True:
            time.sleep(5)
            k+=1
            print('try ',k)
            a2=get_ques()
            print('a2 : ',a2)
            uid=a2[2]
            if uid not in (c.execute("SELECT uid FROM wyr_either").fetchall()):
                print('not in table')
                c.execute("INSERT INTO wyr_either VALUES (:option1,:option2,:date,:uid)", {
                          'option1': a2[0], 'option2': a2[1], 'date': date, 'uid': a2[2]})
                conn.commit()
                conn.close()
                print('^_^ success in try ',k)
                return (a2[0],a2[1])
            else:
                continue
    except Exception as e:
        print(" Error : ",e)
    driver.close()
    
def formimage():
    a2=get_unique_ques()
    a5=FormWyr().get_image(a=a2[0],b=a2[1])
    return [a2[0],a2[1]]






"""    conn = sqlite3.connect('wyr_either.db')
    c = conn.cursor()
    a2=get_ques()
    uid=a2[2]
    if uid not in (c.execute("SELECT uid FROM wyr_either").fetchall()):
        print('not in table')
        a5=FormWyr().get_image(a=a2[0],b=a2[1])
        c.execute("INSERT INTO wyr_either VALUES (:option1,:option2,:date,:uid)", {
                  'option1': a2[0], 'option2': a2[1], 'date': date, 'uid': a2[2]})
        conn.commit()
        conn.close()
    else:
        print('in table')
        a3 = get_ques()
        a5=FormWyr().get_image(a=a3[0],b=a3[1])
        c.execute("INSERT INTO wyr_either VALUES (:option1,:option2,:date,:uid)", {
                  'option1': a3[0], 'option2': a3[1], 'date': date, 'uid': a3[2]})
        conn.commit()
        conn.close()"""
