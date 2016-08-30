#!/usr/bin/python

import ConfigParser
import smtplib
import time
from email.mime.text import MIMEText
from random import randrange


#BEGIN PROCESS CONFIG FILE
Config = ConfigParser.ConfigParser()
Config.read("mailer.ini")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

server = ConfigSectionMap("ServerSettings")
email = ConfigSectionMap("Email")
pool = ConfigSectionMap("Pools")


#END PROCESS CONFIG FILE


#BEGIN IDENTITY GENERATOR
domain = pool["domains"].split()
lastNames = pool["lastnames"].split()
firstNames = pool["firstnames"].split()
text = open(email["text"], "rb")

def createIdentity():
    dict1 = {}
    dict1["firstName"]=firstNames[randrange(0,len(firstNames))]
    dict1["lastName"]=lastNames[randrange(0,len(lastNames))]
    dict1["email"]="".join([dict1["firstName"], ".", dict1["lastName"], "@" ,domain[randrange(0,len(domain))]])
    return dict1
#END IDENTITY GENERATOR


def craftMessage(subject, identity, recipient, text):
    msg = MIMEText(text.read())
    msg['Subject'] = subject
    msg['From'] = identity["email"]
    msg['To'] = recipient
    return msg

def sendMessage(smtp, identity, recipient, message):
    s = smtplib.SMTP(smtp)
    s.sendmail(identity["email"], recipient, (message.as_string()).format(identity["firstName"], identity["lastName"]))
    s.quit()
    print "Mail Sent!"

def execRoutine():
    identity = createIdentity()
    sendMessage(server["smtp"], identity, email["recipient"], craftMessage(email["subject"], identity, email["recipient"], text))

i = int(server["ticks"])
timeout = int(server["timeout"])

while True:
    execRoutine()
    if (i == 1):
        break
    else:
        i-=1
        time.sleep(timeout)
