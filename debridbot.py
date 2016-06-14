#-*- coding:utf-8 -*-
#installare le dipendenze
#python -m pip install --upgrade pip
#pip install pyTelegramBotAPI
#pip install psutil
#pip install requests
import telebot
import subprocess
import psutil
import sys
import requests
from pprint import pprint
from telebot import types
reload(sys)
sys.setdefaultencoding("utf-8")

#admin = [line.rstrip('\n') for line in open('admin.txt','rt')]
API_TOKEN = 'token'
URL = 'http://www.alldebrid.com/register/?action=login&login_login=xxxxxxxx&login_password=xxxxxxxx'
PROCNAME = "a.exe"
bot = telebot.TeleBot(API_TOKEN)

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
def debridit(link):
    session = requests.session()
        # Authenticate
    r = session.get(URL)
    initial_link = 'http://www.alldebrid.com/service.php?json=true&link=%s'%(link)
        # Try accessing a page that requires you to be logged in
        #bot.send_message(cid, 'http://www.alldebrid.com/service.php?json=true&link=%s'%(message.text))
    r = session.get(initial_link)
    var= str(r.content)
    words = var.split(",")
        #print words[0]
    #check empty 
    link = words[0].split("\"")
    final_link = link[3].replace("\\","")
    if str(final_link[-1:]) == '?':
        bot.send_message(cid, 'link non valido')
    else:
        bot.send_message(cid, final_link)
        

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    if isAdmin(cid):
        bot.send_message(cid,"ok")
    else:
        bot.send_message(cid, "NON HAI I PERMESSI")
    

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

@bot.message_handler(commands=['link'])
def link(m):
    cid = m.chat.id
    name = m.from_user.first_name
    if len(m.text.split()) != 2:
        bot.send_message(cid, " /link <LINK>")
        return
    try:
        link = str(m.text.split()[1])
        origLink = link 
    except:
        bot.send_message(cid, " /link <LINK>")
        return
            # Start a session so we can have persistant cookies
    session = requests.session()
        # Authenticate
    r = session.get(URL)
    initial_link = 'http://www.alldebrid.com/service.php?json=true&link=%s'%(link)
        # Try accessing a page that requires you to be logged in
        #bot.send_message(cid, 'http://www.alldebrid.com/service.php?json=true&link=%s'%(message.text))
    r = session.get(initial_link)
    var= str(r.content)
    words = var.split(",")
    #bot.send_message(cid,words[0])
    link = words[0].split("\"")
    if not link[3]:
        link[3] = str('nonvalid?')
    final_link = link[3].replace("\\","")
    if str(final_link[-1:]) == '?':
        bot.send_message(cid, 'link non valido')
    else:
        bot.send_message(cid, final_link)
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
