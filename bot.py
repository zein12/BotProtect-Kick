# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + "Thanks for add")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + "WELCOME to " + group.name)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param3).displayName + " Good Bye\n(*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " Good Bye\n(*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    sendMessage(msg.to,md)
                if "gname:" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Group Name"+key+"Canged to")
	
if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "buka":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "sudah dibuka")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                if msg.text == "tutup":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "sudah ditutup")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL close")
	
