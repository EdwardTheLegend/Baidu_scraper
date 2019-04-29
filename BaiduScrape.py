from selenium import webdriver
from selenium.webdriver.common import keys
import pandas as pd
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-n","--name",default='finaloutput' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),type=str, help="File name for final output, default is finaloutput + the current date. You do NOT need to add file extension."
parser.add_argument("-d","-delay",default=0, help="Optional delay between keywords for slow connections/computers(seconds).")

args = parser.parse_args()

name = args.name
delay = args.delay

df = pd.read_csv('keywords.csv')

#open chrome
driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")

outputfile = []
#print(df)
#print(df.at[3])
def scrape1keyword(kw):
    driver.get("about:blank")
    time.sleep(1)
    driver.get("https://www.baidu.com/")
    time.sleep(3)
    #print("started scrape")
    box = driver.find_element_by_id("kw")
    box.send_keys(kw)
    #print("typed " + kw)
    button = driver.find_element_by_id("su")
    button.click()
    time.sleep(3)
    #print("clicked search")
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