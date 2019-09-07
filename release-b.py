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


def sex_draw(sexlist,mid):
    plt.rcParams['font.sans-serif']=['SimHei']

    countdict = Counter(sexlist)
    sex = []
    num = []
    for s in countdict.keys():
        sex.append(s)
    for n in countdict.values():
        num.append(n)

    plt.figure(figsize=(6,9)) #调节图形大小
    labels = sex #定义标签
    sizes = num #每块值
    if len(sex) == 2:
        colors = ['red','yellowgreen']
        explode = (0.02,0.02) #将某一块分割出来，值越大分割出的间隙越大
    elif len(sex) == 0:
        print('评论不足20，无法分析') 
    elif len(sex) == 1:
        colors = ['pink'] 
        explode = (0.02) 
    elif len(sex) == 3:
        colors = ['pink','yellowgreen','lightskyblue'] 
        explode = (0.02,0.02,0.02) 
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
    plt.title('AV号'+ str(mid) +'的评论者性别画像')
    plt.legend()
    plt.savefig('av'+ str(mid) +'_sex_map.png') #一定放在plt.show()之前
    plt.show()

def level_draw(levellist,mid):
    plt.rcParams['font.sans-serif']=['SimHei']

    countdict = Counter(levellist)
    level = []
    num = []
    for l in countdict.keys():
        level.append(l)
    for n in countdict.values():
        num.append(n)

    plt.figure(figsize=(6,9)) #调节图形大小
    labels = level#定义标签
    sizes = num #每块值
    print(len(level))
    if len(level) == 1:
        colors = ['red']
        explode = (0.02)
    elif len(level) == 2:
        colors = ['pink','yellowgreen']
        explode = (0.02,0.02,0.02) 
    elif len(level) == 3:
        colors = ['pink','yellowgreen','lightskyblue']
        explode = (0.02,0.02,0.02) 
    elif len(level) == 4:
        colors = ['pink','yellowgreen','lightskyblue','red']
        explode = (0.02,0.02,0.02,0.02) 
    elif len(level) == 5:
        colors = ['pink','yellowgreen','lightskyblue','yellow','red']
        explode = (0.02,0.02,0.02,0.02,0.02)
    elif len(level) == 6:
        colors = ['pink','yellowgreen','lightskyblue','red','yellow','green']
        explode = (0.02,0.02,0.02,0.02,0.02,0.02) 
    print(explode)

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
    plt.title('AV号'+ str(mid) +'的评论者等级画像')
    plt.legend()
    plt.savefig('av'+ str(mid) +'_level_map.png') #一定放在plt.show()之前
    plt.show()

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

def main():
    mid = input('视频id: ')
    moder = int(input('模式(1为level画像，2为sex画像): '))
    mainlist = repliesgeter(mid)
    if moder == 1:
        finallist = helper(mainlist,'level')
        level_draw(finallist,mid)
    elif moder == 2:
        finallist = helper(mainlist,'sex')
        sex_draw(finallist,mid)

if __name__ == '__main__':
    main()
