# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:22:03 2018

@author: mahatma.ardika
"""
from requests import get
from bs4 import BeautifulSoup, Comment
import xlsxwriter
#Define the number of the pagination page in detik

def findNewsList(news):
    result = []
    #    define the number of news in a page?
    i = 11
    while i >= 0: 
        news_link_tag = news_list[i].find('a')
        news_link = news_link_tag.get('href')
        response = get(news_link)
        html_news_detail = BeautifulSoup(response.text, 'html.parser')
        news_detail = html_news_detail.find('div',{'class':'detail_text'})
        for element in news_detail(text=lambda text: isinstance(text, Comment)):
            element.extract()
        news_detail.a.decompose()
        news_detail.strong.decompose()
    # replace with `soup.findAll` if you are using BeautifulSoup3
        for div in news_detail.find_all("div", {'class':'pic_artikel pic_artikel_por'}): 
            div.decompose()
        for div in news_detail.find_all("div", {'class':'news_tag'}): 
            div.decompose()
        for div in news_detail.find_all("div", {'class':'detail_tag'}): 
            div.decompose()
        for div in news_detail.find_all("div", {'class':'clearfix mb20'}): 
            div.decompose()
        for div in news_detail.find_all("div", {'class':'lihatjg'}): 
            div.decompose()
        for table in news_detail.find_all("table", {'class':'linksisip'}): 
            table.decompose()
        for script in news_detail.find_all("script"): 
            script.decompose()
        for br in news_detail.find_all("br"): 
            br.decompose()
        for bold in news_detail.find_all("b"): 
            bold.extract()

        news_detail_text = news_detail.text;
        news_detail_clear_1 = news_detail_text.rstrip();
        news_detail_clear_2 = news_detail_clear_1.lstrip();
        news_detail_clear_3 = news_detail_clear_2.replace("\n\t\t\t\t\t\t\t", "")
        news_detail_clear_4 = news_detail_clear_3.replace("(", "")
        news_detail_clear_5 = news_detail_clear_4.replace(")", " ")
        news_detail_clear_6 = news_detail_clear_5.replace("-\n", "")
        news_detail_clear_7 = news_detail_clear_6.replace("\n", "")
        news_detail_clear_8 = news_detail_clear_7.replace("-\t", "")
        #print(news_detail_clear_2)
        news_detail_lower = news_detail_clear_8.lower()  
        news_detail_wt_dot = news_detail_lower.replace(".","")
        news_detail_wt_quote = news_detail_wt_dot.replace('"',"")
        news_detail_wt_comma = news_detail_wt_quote.replace(",","")

        a_news_detail = news_detail_wt_comma.split(" ")
        result.append(a_news_detail)
        i -= 1
    return result

all_news_article = []
i = 1
while i>0:
    index_page = str(i)
    url = 'https://pilkada.detik.com/daerah/all/artikel/'+ index_page 
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    news_containers = html_soup.find_all('ul', {'class': 'list feed bg_white'})
    news_list = news_containers[0].find_all('article')
    result = findNewsList(news_list)
    all_news_article.append(result)
    i -= 1
import xlsxwriter

workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet = workbook.add_worksheet()


row = 0

for col, data in enumerate(all_news_article[0]):
    worksheet.write_column(row, col, data)

workbook.close()