"""
download and replace links.txt with the new links
download link -> https://github.com/viveks-codes/viveks-codes/blob/master/links.txt
If you want to create links.txt on your own then you can use this notebook
templates/linksgenration.ipynb
"""
# import beautifulsoup4
import requests
from bs4 import BeautifulSoup
import json
#now read file links.txt and get soup from each link
with open('links.txt', 'r') as f:
    links = f.readlines()
    links = [x.strip() for x in links]
for i in range(0,len(links)):
    r = requests.get(links[i])
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.prettify())
    #scrape a tag having class crayons-link fw-bold
    usernametag = soup.find_all('a', class_='crayons-link fw-bold')
    # get href 
    username = usernametag[0].get('href')
    #print(username)
    # get all p tags having class fs-xs color-base-60
    date = soup.find_all('p', class_='fs-xs color-base-60')
    
    # remove all white spaces from starting
    date = date[0].text.lstrip()
    


    #print(date)
    # get all h1 tags having class fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 medium or fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 longer or fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 small
    title = soup.find_all('h1', class_='fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 medium')
    if len(title) == 0:
        title = soup.find_all('h1', class_='fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 longer')
    if len(title) == 0:
        title = soup.find_all('h1', class_='fs-3xl m:fs-4xl l:fs-5xl fw-bold s:fw-heavy lh-tight mb-2 short')
    # get text
    
    #print(title[0].text)
    # get all text with dev tag and class is crayons-article__main
    content = soup.find_all('div', class_='crayons-article__main')
    # get text
    #print(content[0])
    #save username, date, title, content in html file title.txt 
    with open('Articals/'+(title[0].text).lstrip().rstrip().replace(" ",'-')+'.html', 'w') as f:
        f.write("<h1>")
        f.write(str(title[0].text))
        f.write("</h1>")
        f.write("<p>")
        f.write(str(date))
        f.write("</p>")
        f.write("<p>")
        f.write(str(content[0]))
        f.write("</p>")
        f.write("<p>")
        f.write(str(username))
        f.write("</p>")
print("{} artical added at AskaDev/templates/Articals".format(i+1))