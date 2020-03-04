import os, re, requests, time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Initialize the lists 
name_video=[]
vis_video=[]
link=[]

# Open Youtube Video Channel
thing_url=input('Youtube Channel Link: ')
if thing_url[-6:]!='videos':
    if thing_url[-1]=='/':
        thing_url=thing_url+'videos'
    else:
        thing_url=thing_url+'/videos'


# Initialize browser
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(thing_url)

# Scroll to the end of the page
time.sleep(1.5)
SCROLL_PAUSE_TIME = 1
# Get scroll height
height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == height:
        break
    height = new_height
    
# Extract source code
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, "html.parser")
titulo = soup.title.text

antes="oi"
for lista in soup.findAll(class_='style-scope ytd-grid-video-renderer'):
    titulo_bruto=lista.find("a", {"id" : "video-title"})
    #print(titulo_bruto)
    try:
        if titulo_bruto.text!=antes:
            #print(titulo_bruto.text)
            name_video.append(titulo_bruto.text)
            antes=titulo_bruto.text
            label=str(titulo_bruto)
            numero_visualizacoes= ''.join(re.findall(r'([0-9.]*) visualizações', label))
            numero_visualizacoes=numero_visualizacoes.replace('.','')
            #print(numero_visualizacoes)
            vis_video.append(numero_visualizacoes)
            links= ''.join(re.findall(r'href="([a-zA-Z0-9?=/\-_]*)', label))
            links='https://www.youtube.com'+links
            link.append(links)
            #print('\n\n')
    except:
        continue
        
# Create CSV File
for i in range(0,len(name_video)):
    combinacao=[name_video[i],vis_video[i], link[i]]
    df=pd.DataFrame(combinacao)
    with open(titulo+'.csv', 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='iso-8859-1', header=False, sep = "\t", index=False)
        
# Adjust CSV File - Descending Order of "View"
data=pd.read_csv(titulo+'.csv', encoding='utf-16', header=None, sep = "\t") 
data.sort_values(1, axis=0, 
                 ascending=False, inplace=True) 
data.to_csv(open(titulo+'.csv','w',encoding='utf-16', newline=''), encoding='iso-8859-1', header=False, sep = "\t", index=False)

# Number of total videos from channel        
print("Total videos: " + str(len(name_video)))

driver.quit()