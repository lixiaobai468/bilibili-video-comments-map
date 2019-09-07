import json
import requests
from collections import Counter
from matplotlib import pyplot as plt

def getAllAVList(mid, size, page):
    '''
    [avid,...]
    '''
    # 获取UP主视频列表
    for n in range(1,page+1):
        url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
            str(mid) + "&pagesize=" + str(size) + "&page=" + str(n)
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        aid_list = []
        for item in json_text["data"]["vlist"]:
            aid_list.append(item["aid"])
    return aid_list

def repliesgeter(mid):
    '''
    {msg,uname,mid,sex}
    '''
    mainjson = json.loads(requests.get('http://api.bilibili.com/x/reply?type=1&oid='+ str(mid) +'&pn=1&nohot=1&sort=0').text)
    
    r_count = mainjson['data']['page']['count']
    #print(r_count)
    p_count = r_count // 20 + 1 
    #print(p_count)
    
    rlist = list()
    for page in range(1,p_count):
        geturl = 'http://api.bilibili.com/x/reply?type=1&oid='+ str(mid) +'&pn='+ str(page) +'&nohot=1&sort=0'
        print(geturl)
        replyfull = json.loads(requests.get(geturl).text)['data']['replies']
        for n in range(0,20):
            rlist.append({'msg':replyfull[n]['content']['message'],'uname':replyfull[n]['member']['uname'],'mid':replyfull[n]['member']['mid'],'sex':replyfull[n]['member']['sex'],'level':replyfull[n]['member']['level_info']['current_level']})
    return rlist

def helper(manlist,mode='sex'):
    lister = []
    if mode == 'sex':
        for member in manlist:
            lister.append(member['sex'])
        return lister
    elif mode == 'level':
        for member in manlist:
            lister.append(member['level'])
        return lister
    else:
        raise Exception('The value of "mode" must be "sex" or "level".')

def main(uid):
    midlist = getAllAVList(uid, 20, 1)
    s_per_list = []
    for mid in midlist:
        mainlist = repliesgeter(mid)
        sexlist = helper(mainlist,'sex')

        countdict = Counter(sexlist)
        sex = []
        num = []
        for s in countdict.keys():
            sex.append(s)
        for n in countdict.values():
            num.append(n)
        
        per = [p/sum(num) for p in num]
        perdict = {a:b for a,b in zip(sex,per)}
        if perdict != {}:
            s_per_list.append(perdict)
    
    man = 0
    woman = 0
    secret = 0
    mlist = []
    wlist = []
    slist = []
    for ov in s_per_list:
        if '男' in ov:
            man += 1
            mlist.append(ov['男'])
        if '女' in ov:
            woman += 1
            wlist.append(ov['女'])
        if '保密' in ov:
            secret += 1
            slist.append(ov['保密'])

    manper = sum(mlist)/man
    womanper = sum(wlist)/woman
    secretper = sum(slist)/secret
    
    allper = [manper,womanper,secretper]

    plt.rcParams['font.sans-serif']=['SimHei']

    plt.figure(figsize=(6,9)) #调节图形大小
    labels = ['男','女','保密'] #定义标签
    sizes = allper #每块值
    colors = ['lightskyblue','pink','yellowgreen'] #每块颜色定义
    explode = (0.02,0.02,0.02) #将某一块分割出来，值越大分割出的间隙越大
    patches,text1,text2 = plt.pie(sizes,
                        explode=explode,
                        labels=labels,
                        colors=colors,
                        autopct = '%3.2f%%', #数值保留固定小数位
                        shadow = True, #无阴影设置
                        startangle =90, #逆时针起始角度设置
                        pctdistance = 0.6) #数值距圆心半径倍数距离
    #patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.title('UID'+ str(uid) +'的最新20视频评论者性别画像')
    plt.legend()
    plt.savefig('UID'+ str(uid) +'_sex_map.png') #一定放在plt.show()之前
    plt.show()

if __name__ == '__main__':
    main(295723)
