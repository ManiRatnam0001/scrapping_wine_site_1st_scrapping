import requests as r
from bs4 import BeautifulSoup as bs
from bs4 import XMLParsedAsHTMLWarning
import warnings
import json
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
url="https://chambersstwines.com/sitemap.xml"
def mn_lnk():
    res=r.get(url)
    link=[]
    if res.status_code==200:
        soup=bs(res.text,'lxml')
        for char in soup.find_all('loc'):
            char =char.text
            link.append(char)
        for var in link:
            if len(var) != 86:
                link.remove(var)
        lnk_col_cat=link.pop()
        return link
def col_url():
    sub_lnk=[]
    for url in mn_lnk():
        nxt_res=r.get(url)
        prtfy=bs(nxt_res.text,'lxml')
        for var in prtfy.find_all('loc'):
            var=var.text
            sub_lnk.append(var)
    sub_lnk.pop(0)
    return sub_lnk
def parse():
    file_main = open("parsing1.json", "w")
    id=0
    for ele in col_url():
        or_lnk=r.get(ele)
        gt_sp=bs(or_lnk.text,'lxml')
        id+=1
        product_id=gt_sp.find("h1").text.split("\n")[2].lstrip()
        Availability=gt_sp.find("div",class_="product-inventory").text.split("\n")[8].lstrip()
        Price=gt_sp.find("span",class_="price").text.split("\n")[1].lstrip()
        Wine_type=gt_sp.find(class_="product-type").span.text.replace('\n',"").strip()
        def img_url():
            if gt_sp.find("a",class_="fancybox"):
                return "https:"+gt_sp.find("a",class_="fancybox").get("href")
            else:
                return "Not Found"
        attr={
            "id":id,
            'product_id':product_id,
            'Availability':Availability,
            'Price':Price,
            'Wine_type':Wine_type,
            'img_url':img_url()
        }
        json.dump(attr,file_main,indent=6)
        print(attr)
    file_main.close()

 col_url()

