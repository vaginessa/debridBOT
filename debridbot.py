#-*- coding:utf-8 -*-
#installare le dipendenze
#python -m pip install --upgrade pip
#pip install pyTelegramBotAPI
#pip install psutil
#pip install requests
#pip install pyshorteners
import telebot
import subprocess
import psutil
import json
import sys
import requests
from pyshorteners import Shortener
from pprint import pprint
from telebot import types
from telebot import util
reload(sys)
sys.setdefaultencoding("utf-8")

#admin = [line.rstrip('\n') for line in open('admin.txt','rt')]
API_TOKEN = 'token'
URL = 'http://www.alldebrid.com/register/?action=login&login_login=xxxxxx&login_password=xxxxxx'
PROCNAME = "a.exe"
bot = telebot.TeleBot('xxxxxxx')
#google shortner api
api_key='xxxxxxx'
shortener = Shortener('Google', api_key=api_key)
admin = [line.rstrip('\n') for line in open('admin.txt','rt')]
log = [line.rstrip('\n') for line in open('log.txt','rt')]

def addAdmin(name,id):
    global admin
    with open('admin.txt', 'a+') as f:
        f.write("\n"+str(name)+"\n"+str(id))
    #refresh admin list
    admin = [line.rstrip('\n') for line in open('admin.txt','rt')]

def logLink(name,id,OrigLink,DebridLink):
    global log
    with open('log.txt', 'a+') as f:
        f.write(str(name)+"|"+str(id)+"|"+str(OrigLink)+"|"+str(DebridLink)+"\n")
    #refresh admin list
    log = [line.rstrip('\n') for line in open('log.txt','rt')]
    
def isAdmin(var):
    #bot.send_message(var, "%s"%(var))
    #bot.send_message(var, "%s"%(admin))
    if str(var) in admin:
        
        return True
    else:
        return False        

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    cid = message.chat.id
    slash = "/"
    markup = types.ReplyKeyboardMarkup(selective=False)
    #bot.send_message( cid, "Questo bot permette di generare link premium, supporta tutti gli Hoster di ALLDEBRID")
    if isAdmin(cid):
        bot.send_message(cid,"sei admin")
        itembtn1 = slash + "id"
        itembtn2 = slash + "addAdmin"
        itembtn3 = slash + "log"
        markup.add(itembtn1, itembtn2,itembtn3)
        bot.send_message(cid, "Ciao %s hai eseguito l'accesso come admin, cosa vuoi fare?"%(message.from_user.first_name), reply_markup=markup)
        #vedere log
        
        
    else:
        bot.send_message( cid, "Questo bot permette di generare link premium,\n supporta tutti gli Hoster di ALLDEBRID")
        itembtn1 = slash + "id"
        markup.add(itembtn1)
        #bot.send_message(cid, "Ciao %s non sei admin, se lo vuoi diventare manda il tuo Dream"%(message.from_user.first_name), reply_markup=markup)

@bot.message_handler(commands=['id'])
def id(m):
    cid = m.chat.id
    bot.send_message( cid, "Ciao %s , il tuo  ID e' %s.\n" %(m.from_user.first_name, cid))

@bot.message_handler(commands=['admin'])
def id(m):
    cid = m.chat.id
    name = m.from_user.first_name
    if isAdmin(cid) :
        #bot.send_message( cid, "Ciao %s , sei un admin\n" %(m.from_user.first_name))
        bot.send_message( cid, "%s" %(admin))
    else:
        bot.send_message( cid, "Ciao %s , NON sei un admin\n" %(m.from_user.first_name))
    pass

@bot.message_handler(commands=['log'])
def log(m):
    cid = m.chat.id
    if isAdmin(cid) :
        
        doc = open('log.txt', 'rb')
        bot.send_document(cid, doc)
    else:
        bot.send_message( cid, "Ciao %s , NON sei un admin\n" %(m.from_user.first_name))
    pass


@bot.message_handler(regexp='((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
def linkv4(m):
    cid = m.chat.id
    name = m.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    link = str(m.text)
    origLink = link 
    session = requests.session()
    r = session.get(URL)
    r = session.get('http://www.alldebrid.com/service.php?json=true&link=%s'%(link))
    var= str(r.content)
    data = json.loads(var)
    final_link = str(data["link"]).replace(" ","%20")
    if data["link"] != "":
        if str(data["error"]) != "This link isn't valid or not supported.":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(data["filename"]+' ', url="%s"%(final_link)))
            bot.send_message(cid, "Ciao %s ecco il tuo file"%(name), reply_markup=markup)
            logLink(name,cid,origLink,final_link)
    
    pass


@bot.message_handler(commands=['addAdmin'])
def setNewAdmin(m):
    cid = m.chat.id
    if len(m.text.split()) != 3:
        bot.send_message(cid, " /addAdmin <NOME> <ID>")
        return
    try:
        idNADMIN = int(m.text.split()[2])
        name = str(m.text.split()[1])
    except:
        bot.send_message(cid, " /addAdmin <NOME> <ID>")
        return
    bot.send_message(cid, "{} è stato aggiunto agli amministratori con il codice id {}".format(name,idNADMIN))
    addAdmin(name,idNADMIN)
    pass
    
		

bot.polling()
