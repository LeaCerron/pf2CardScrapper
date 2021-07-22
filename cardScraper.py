
import requests
from bs4 import BeautifulSoup
import re


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

alchemicalLinks = ['https://2e.aonprd.com/Equipment.aspx?Category=6&Subcategory=7','https://2e.aonprd.com/Equipment.aspx?Category=6&Subcategory=8','https://2e.aonprd.com/Equipment.aspx?Category=6&Subcategory=9','https://2e.aonprd.com/Equipment.aspx?Category=6&Subcategory=10','https://2e.aonprd.com/Equipment.aspx?Category=6&Subcategory=47']
icons = ['bomb.png','elixer.png','poison.png','tool.png','drug.png']


Html_file= open("cards.html","w")
Html_file.write('<head>\
<link rel="stylesheet" href="cardstyle.css">\
<style>\
</style>\
</head>')
Html_file.close()

for x in alchemicalLinks:
    url = x
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html5lib')

    for row in soup.findAll('table',{'id':'ctl00_MainContent_Rad_AllEquipment_ctl00'})[0].tbody.findAll('tr'):
        r = row.findAll('td')
        if len(r) < 1:
            continue
        first_column = row.find('a')['href']
        
        print(first_column)
        url = first_column
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html5lib')
        for div in soup.find_all("img", {'class':'actionlight'}): 
            div.decompose()
        for div in soup.find_all("a", {'class':'external-link'}): 
            div.decompose()
        # for div in soup.find_all("h2"): 
        #     div.decompose()
        # for div in soup.find_all("h3"): 
        #     div.decompose()
        card = str(soup.find("span", { "id" : "ctl00_MainContent_DetailedOutput" }))

        card = re.sub(r'<h\d class="title">This Item is from [a-zA-Z0-9_ ]* and may contain Spoilers</h\d>', '', card)
        card = card.replace("h1", "h4")
        card = re.sub(r'<img alt="PFS Standard" src="Images\\Icons\\PFS_Standard.png" style="height:\d\dpx; padding:2px 10px 0px 2px" title="PFS Standard"/>','',card)
        card = re.sub(r'<img alt="PFS Limited" src="Images\\Icons\\PFS_Limited.png" style="height:\d\dpx; padding:2px 10px 0px 2px" title="PFS Limited"/>','',card)
        card = re.sub(r'<img alt="PFS Restricted" src="Images\\Icons\\PFS_Restricted.png" style="height:\d\dpx; padding:2px 10px 0px 2px" title="PFS Restricted"/>','',card)
        card = card.replace('<br/><b>Source</b>  <sup></sup>','')
        card = card.replace('<br/><b>Source</b>','')
        card = card.replace('<u><a href="PFS.aspx"><b><i>PFS Note</i></b></a></u><i> Players can gain access to faction-specific gear by taking the corresponding Faction Gear Access Game Reward, available when they reach 20 reputation with the respective faction.</i><br/><br/>', '')
        card = card.replace('<b>Source</b>','')
        card = card.replace('<br/><b>Price</b>','<b>Price</b>')
        card = card.replace('<h4 class="title">', '<h4 class="title"><a href="PFS.aspx"><span style="float:left;"><img alt="PFS Standard" src="Images\Icons\\'+icons[alchemicalLinks.index(x)]+'" style="height:25px; padding:2px 10px 0px 2px" title="PFS Standard"></span></a>')


        Html_file= open("cards.html","a")
        Html_file.write('<div style="width:30%;display:inline-block;margin-right:20px;">')
        Html_file.write(card)
        Html_file.write('</div>')
        Html_file.close()


# print(card)