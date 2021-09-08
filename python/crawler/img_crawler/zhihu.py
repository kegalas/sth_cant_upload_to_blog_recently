import requests
import json
import re
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}

param = {
    'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
    'limit':'5',
    'offset':'0',
    'platform': 'desktop',
    'sort_by': 'default',
}

counter_offset = 0
counter_img_total = 0

i=0

while i<110:
    offset_answer = -1
    i+=1
    url = 'https://www.zhihu.com/api/v4/questions/484926831/answers'
    param['offset'] = counter_offset
    response2 = requests.get(url=url,headers=headers,params=param)
    data = json.loads(response2.text)

    pattern = re.compile(r'https://pic.\.zhimg\.com/v2-.{32}_r\.jpg')
    
    while offset_answer<4:
        offset_answer+=1
        result = pattern.findall(str(data['data'][offset_answer]['content']))
        img_url = list(set(result))

        counter_img_now = 0

        while len(img_url)>0 and counter_img_now<len(img_url):
            counter_img_total+=1
            counter_img_now+=1
            img = requests.get(url=img_url[counter_img_now-1],headers=headers,stream=True)
            f = open('./img/{}.jpg'.format(counter_img_total),'wb')
            f.write(img.content)
            f.close()
    
    counter_offset += 5 
    time.sleep(1)

    