#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import poplib
import os
import datetime
import logging
import traceback
import urllib2
import json
from email.parser import Parser
from email.header import decode_header

email = 'xuhaoqi9310@163.com'
password = 'xxxx'
pop3_server = 'pop.163.com'
developers = {"xuhaoqi9310@163.com":18800000000,"genuinex@demo.com":18800000000}
serverDevs = ["genuine@demo.com"]

logging.basicConfig(level=getattr(logging, 'INFO'),
       format='%(asctime)s %(filename)s[line:%(lineno)d] %(name)s %(levelname)s %(message)s',
       datefmt='%m-%d %H:%M:%S',
       filename='/tmp/checkEmail.log',
       filemode='a')

def decode_str(s,index):
    #print decode_header(s)
    value, charset = decode_header(s)[index]
    if charset:
        value = value.decode(charset)
    return value

def get_from_add(fromAdd):
    begin = fromAdd.find('<')
    end = fromAdd.find('>')
    return fromAdd[begin+1:end]

def send_notice(data):
    req = urllib2.Request('https://www.linkedsee.com/alarm/channel')
    req.add_header('Servicetoken','85d9698ce97c7a00000000eadb5f0f1d') #change your token
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

def check_email_receive():
    try_num = 1
    server = None
    logging.info('Begin check email receive !!!')
    while try_num != 0:
        try_num = try_num - 1
        try:
            server = poplib.POP3(pop3_server,110,10)
            #server = poplib.POP3_SSL(pop3_server,'995')
            server.user(email)
            auth = server.pass_(password)
            #emailMsgNum, emailSize = server.stat()
            #print  'email number is %d and size is %d'%(emailMsgNum, emailSize)  
            resp, mails, octets = server.list()
            index = len(mails)
            while index:
                resp, lines, octets = server.retr(index)
                msg_content = '\r\n'.join(lines)
                msg = Parser().parsestr(msg_content)
                #print msg
                indexA = msg.get('date','').find("+")
                if msg.get('date','').find(",") == -1:
                    DateData = datetime.datetime.strptime(msg.get('date','')[:indexA-1],"%d %b %Y %H:%M:%S")
                else:
                    DateData = datetime.datetime.strptime(msg.get('date','')[:indexA-1],"%a, %d %b %Y %H:%M:%S")
                TodayData = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                if DateData < TodayData:
                    break

                SubData = decode_str( msg.get('subject',''),0)
                if SubData.find(u'_日报_') > -1:
                    #print SubData,
                    #FromData = decode_str(msg.get('from',''),0)
                    FromData = get_from_add(msg.get('from',''))
                    #print FromData
                    if developers.has_key(FromData):
                        developers[FromData] = "sended"
                index = index - 1

            serverDevFlag = True
            for developer in developers:
                if developer!="xuhaoqi@linkedsee.com" and developers[developer] != "sended":
                    if developer in serverDevs:
                        serverDevFlag = False
                    logging.info("%s not send email" % developer)
                    dataToPost = {}
                    dataToPost['receiver'] = developers[developer]
                    nowHour = datetime.datetime.now().hour
                    dataToPost['type'] = u'sms'
                    if nowHour > 20:
                        dataToPost['type'] = u'phone'
                    dataToPost['title'] = u'日报提醒'
                    dataToPost['content'] = '少年发日报啊！发日报啊！发日报啊！发日报啊！发日报啊！'
                    logging.info(send_notice(json.dumps(dataToPost)))

            if developers["xuhaoqi@linkedsee.com"]!= "sended"  and serverDevFlag:
                dataToPost = {}
                dataToPost['receiver'] = developers["xuhaoqi@linkedsee.com"]
                nowHour = datetime.datetime.now().hour
                dataToPost['type'] = u'sms'
                if nowHour > 20:
                    dataToPost['type'] = u'phone'
                dataToPost['title'] = u'日报提醒'
                dataToPost['content'] = '日报已经收齐，请发日报。'
                logging.info(send_notice(json.dumps(dataToPost)))

            server.quit()
        except Exception, e:
            logging.exception('Check email reveive exception, %s' % (traceback.format_exc()))
    logging.info('Finish check email receive !!!')

if __name__ == '__main__':
    check_email_receive()
