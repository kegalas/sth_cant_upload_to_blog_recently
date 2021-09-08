import requests
import json
import re
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from wordcloud import WordCloud
import sys

url = 'https://www.zhihu.com/api/v3/moments/vladimir-90-83/activities?before_id=1630820534&limit=7&session_id=1418504097955377152&desktop=true'
font = r'C:\Windows\Fonts\msyh.ttc'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}

keywords_list = list()
keywords_string = str()

def get_keywords(question_url):
    html = urlopen(question_url)
    bs = BeautifulSoup(html.read(),'html.parser')
    keywords_html = bs.find('meta',{'itemprop':'keywords'})
    all_keywords_string = keywords_html['content']+','#提取关键词content，加个逗号是依据下面的提取算法来设置的
    each_word = ''  #为了将一个个单字合成为一个词语而设立的字符串
    for word in all_keywords_string:
        if word != ',':
            each_word = each_word + word
        else:
            keywords_list.append(each_word)
            global keywords_string
            keywords_string += each_word + ' '
            each_word=''
            


for j in range(0,100):
    try:
        response = requests.get(url=url,headers=headers)
        data = json.loads(response.text)
        pattern = re.compile(r'\d+')
        for i in range(0,7):
            try:
                question_url = 'https://www.zhihu.com/question/'+pattern.findall(data['data'][i]['target']['question']['url'])[0]
                print(question_url)
                get_keywords(question_url)
                #print(keywords_list)
                #print(keywords_string)
                time.sleep(2)
            except KeyError:
                print('不是问题是文章')
                time.sleep(2)
        if data['paging']['is_end'] == True:
            break
        url = data['paging']['next']
    except:
        print("Unexpected error:", sys.exc_info()[0])
        continue

wc = WordCloud(
    font_path=font,
    width=5000,
    height=5000,
)

wc.generate(keywords_string)
wc.to_file('ss.png')






