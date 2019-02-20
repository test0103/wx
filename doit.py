import hashlib

from flask import Flask, request, make_response

import time
import xml.etree.ElementTree as et
app = Flask(__name__)
app.debug = True
text_str = '''<xml>
            <ToUserName>![CDATA[%s]]</ToUserName>
            <FromUserName>![CDATA[%s]]</FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType>![CDATA[text]]</MsgType>
            <Content>![CDATA[%s]]</Content>
            </xml>''' 
def reply(type): 
    if type == 'text': 
        return text_str

@app.route('/')
def hello():
	return 'hey'

@app.route('/wx',methods=['GET','POST'])
def wechat():
    if request.method == 'POST':
        print('post')
        xml_recv = et.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text   #获取之前发送的 目标用户（公众号）
        FromUserName = xml_recv.find("FromUserName").text #获取之前的 消息来源用户
        Content = xml_recv.find("Content").text     #获取之前 向服务器发送的消息
        #构造xml格式，回复内容
        reply = """<xml>
                <ToUserName> <![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>"""
        response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response                 #返回这个xml消息
    else :
        print('get')
        return 'get'
if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=80)
