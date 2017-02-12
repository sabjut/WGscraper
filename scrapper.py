#!/bin/python3

from bs4 import BeautifulSoup
import requests
import re

class WG:
    title=""
    price=""
    people=""
    deposit=""
    size=""
    address=""
    availabledate=""
    gender=""
    minage=""
    maxage=""
    text=""

    def print(self):
        print(
                                  self.title         +"\n"+
            "Rent: "            + self.price         +"\n"+
            "Deposit: "         + self.deposit       +"\n"+
            "People: "          + self.people        +"\n"+
            "Size: "            + self.size          +"\n"+
            "Address: "         + self.address       +"\n"+
            "From"              + self.availabledate +"\n"+
            "Searching for: "   + self.gender +" from "+ self.minage +" to "+ self.maxage +"\n\n"+
            self.text +"\n"
        )

def run(url):
    sitelist = []
    soup = getSoup(url)

    if (soup.title.getText() == "Überprüfung"):
        print ("They hate bots :(")
        return

    maxsites = getmaxsites(soup)
    for i in range(0, maxsites):
        newsites = getSites(soup)
        for site in newsites:
            wg = getInfo(getSoup("http://www.wg-gesucht.de/" + site))
            wg.print()
        sitelist += newsites
        url = url.replace(str(i) + ".html", str(i+1) + ".html")
        soup = getSoup(url)

def getSoup(url):
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.21 Safari/537.36',})
    html = requests.get(url, headers=headers).content
    return BeautifulSoup(html, "html.parser")


def getSites(soup):
    sitelist = []
    for item in soup.find_all("tr", id=["ad--0", "ad--1"]):
        sitelist.append(item['adid'])
    return sitelist

def getmaxsites(soup):
    btns = soup.find("ul", class_="pagination pagination-sm").find_all("li")
    return int(btns[len(btns) - 2].a.getText().strip())

def getInfo(soup):
    wg = WG()
    print(soup.title.getText())
    print(soup.select("span.headline-detailed-view-title"))
    #wg.people = soup.find_all("span", class_="headline-detailed-view-title")[0].span['title']
    #wg.size = soup.find_all("h1", class_="headline headline-orange")[0].getText()
    #wg.price = soup.find_all("h1", class_="headline headline-orange")[1].getText()

    return wg

run("https://www.wg-gesucht.de/wg-zimmer-in-Berlin.8.0.0.0.html")
