#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-16

import json
import requests
import cx_Oracle
import datetime

# 微信公众号上应用的CropID和Secret
corpid = 'wx8d46d36104988993'
corpsecret = 'fm2SOjoOGI8HrOb2n3S1r4OE9G5R52I1aGWFnVpTd-E'
# 各项目组编号
fujia = 'XS3007'
mikailuo = 'XS3008'
haerbin_control = 'XS3003'
haerbin_expose = 'XS3031'

# 获取问卷项目数据
def get_wenjuan(project_num):
    # 创建一个数据库连接
    try:
        conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    except:
        print("无法连接数据库")
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select A.allcount,B.allvisit,c.yestvisit,d.dvisit,e.cvisit,f.svisit from 
(select count(distinct(comuid)) as allcount from T_PROJECT t where t.pid='%s' and menu='C')  A,
(select count(distinct(comuid)) as allvisit from T_PROJECT t where t.pid='%s' and status='10')  B,
(select count(distinct(comuid)) as yestvisit from T_PROJECT t where t.pid='%s' and status='10' and  trunc(CREATE_TIME)=trunc(sysdate-1))  C,
(select count(distinct(comuid)) as dvisit from T_PROJECT t where t.pid='%s' and menu='Q') D,
(select count(distinct(comuid)) as cvisit from T_PROJECT t where t.pid='%s' and menu='C') E,
(select count(distinct(comuid)) as svisit from T_PROJECT t where t.pid='%s' and menu='S') F""" % (project_num,project_num,project_num,project_num,project_num,project_num))

    one = cursor.fetchone()
    conn.close()
    cursor.close()
    return one

# 获取微信接口token
def getToken(corpid,corpsecret):
    # 获取access_token
    GURL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(GURL).json()['access_token']
    return token

# 向接口发送消息
def sendMsg(title,message):
    # 获取access_token
    access_token = getToken(corpid,corpsecret)
    # 消息发送接口
    Purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"  % access_token
    # 要发送的消息
    weixin_msg = {
        "toparty": '2',      # 部门ID
        "agentid": '1000005',   # 企业应用的id
        "msgtype" : "textcard",
        "textcard": {
            "title": title,
            "description": message,
            "url": "www.wzlinux.com",
            "btntxt": "更多"
        }
    }
    # 向消息接口发送消息
    print(requests.post(Purl,data = json.dumps(weixin_msg),headers={'Content-Type': 'application/json;charset=utf-8'}).content)

def send_pijiu(x,wenjuan_data):
    a,b,c,d,e,f = wenjuan_data
    title = x
    message = "截止到%s日\n总完成数：%d\n总访问数：%d\n昨日访问数：%d\n配额满：%d\n完成：%d\n甄别：%d" % ( datetime.date.today(),a,b,c,d,e,f)
    sendMsg(title,message)


if __name__ == '__main__':
    send_pijiu('米凯罗啤酒',get_wenjuan(mikailuo))
    send_pijiu('福佳啤酒',get_wenjuan(fujia))
    send_pijiu('哈尔滨啤酒控制组',get_wenjuan(haerbin_control))
    send_pijiu('哈尔滨啤酒曝光组',get_wenjuan(haerbin_expose))
