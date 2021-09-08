import requests
import json
import time


param = {#ajax请求的参数
    'vmid': '1',
    'jsonp':'jsonp',
}

param2 = {#ajax请求的参数
    'mid': '1',
    'jsonp':'jsonp',
}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}


i = 2002

while True:
    param['vmid'] = '{}'.format(i)
    param2['mid'] = '{}'.format(i)

    url = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(i)
    response = requests.get(url=url,params=param,headers=headers)

    url2 = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(i)
    response2 = requests.get(url=url2,params=param2,headers=headers)

    try:
        data = response.text
        data = json.loads(data)

        data2 = response2.text
        data2 = json.loads(data2)

        print('用户名: {}'.format(data2['data']['name']),end='    ')
        print('uid: {}'.format(i),end='    ')
        print('关注数: {}'.format(data['data']['follower']))
    
        fo = open('fans_bili.txt',"a")
        fo.write('用户名: {}    '.format(data2['data']['name']))
        fo.write('uid: {}    '.format(i))
        fo.write('关注数: {}\n'.format(data['data']['follower']))
        fo.close()
    except KeyError:
        print('该用户不存在!')
    
    i+=1
    time.sleep(1)






