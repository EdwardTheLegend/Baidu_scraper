from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import argparse
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("-n","--name",default='finaloutput' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),type=str, help="File name for final output, default is finaloutput + the current date. You do NOT need to add file extension.")
parser.add_argument("-d","--delay",default=0, help="Optional delay between keywords for slow connections/computers(seconds).")
parser.add_argument("-k","--keywords",default="keywords.csv", help="Optional specify path to keywords, default is keywords.csv")

args = parser.parse_args()

name = args.name
delay = args.delay
keywords = args.keywords

df = pd.read_csv(keywords)

#open chrome
driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")

outputfile = []
#print(df)
#print(df.at[3])
def scrape1keyword(kw):
    driver.get("about:blank")
    time.sleep(delay)
    driver.get("https://www.baidu.com/")
    time.sleep(delay)
    #print("started scrape")
    box = driver.find_element_by_id("kw")
    box.send_keys(kw)
    time.sleep(delay)
    print("typed " + kw)
    time.sleep(delay)
    button = driver.find_element_by_id("su")
    button.click()
    time.sleep(delay)
    #print("clicked search")

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-showurl')))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time!"

    urls = driver.find_elements_by_class_name("c-showurl")
    #print("got urls list")
    i = 1
    for url in urls:
        # output line will look like this
        # 1,"word","ttp://exampe.com/"
        output1line = str(i) + ",\"" + kw + "\",\"" + url.text + "\"" 
        #print("going to print output")
        outputfile.append(output1line)
        #print("printed output")
        i += 1

for kw in df.Words:
    #print("this is kw: " + kw)
    scrape1keyword(kw)
    time.sleep(delay)

outfiledf = pd.DataFrame(outputfile)
outfiledf.to_csv(name + '.csv')
#print("end")