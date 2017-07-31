from getpass import getpass
from urllib import parse as urlparse
import os
import io
import urllib
import threading
from Queue import Queue

fburl = 'https://m.facebook.com'

def interactive_login(browser,msg=""):
    #this is because we don't wanna deal
    #with all the crap FB can throw up
    #like this one tap login thing
    browser.get(fburl)
    try:
        browser.execute_script('alert("Log in manually pls, then press ENTER on the command line.")')
    except:
        pass
    input(msg)


#let's start the fun stuff
#TODO: go to next page of thread list
#TODO: detect last page
def conversation_pages(browser):
    pageNum=0
    while True:
        url=(fburl+'/messages/?pageNum=%d')%(pageNum,)
        browser.get(url)
        links=map(lambda e: e.get_attribute('href'),
                  browser.find_elements_by_tag_name('a'))
        threads=list(filter(lambda l: str(urlparse.urlsplit(l).path).startswith('/messages/read'), links))
        if len(threads)==0:
            #no more threads
            return
        else:
            yield url
        pageNum+=1

def conversations_on_page(browser,url):
    browser.get(url)
    links=list(map(lambda e: e.get_attribute('href'),
              browser.find_elements_by_tag_name('a')))
    return filter(lambda l: str(urlparse.urlsplit(l).path).startswith('/messages/read'), links)

def conversation_id(url):
    return str(urlparse.parse_qs(urlparse.urlsplit(url).query)['tid'])

def conversation_name(browser,url):
    browser.get(url)
    return browser.title

#WARNING: This is in reverse chronological order
def pages_in_conversation(browser,url):
    browser.get(url)
    while True:
        older=browser.find_elements_by_id('see_older')
        if len(older)==0:
            yield url
            break
        else:
            nexturl=older[0].find_element_by_tag_name('a').get_attribute('href')
            yield url
            url=nexturl
            browser.get(url)

#reverses order and removes extra stuff
def reverse_html_of_conversation_page(browser,url):
    browser.get(url)
    script='''
    return (function(){
        let l=document.getElementById('messageGroup').children[1].children;
        let src="";
        for (let i=l.length-1; i>=0; i--) {
            src+=l[i].innerHTML;
        }
        return src;
    })();
    '''
    return browser.execute_script(script)

#shamelessly copied from stackoverflow
class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception,e:
                print "   Error: %s"%e
            self.queue.task_done()

    def download_url(self, url):
        # change it to a different way if you require
        name = url.split('/')[-1]
        dest = os.path.join(self.destfolder, name)
        print( "[%s] Downloading %s -> %s"%(self.ident, url, dest))
        urllib.urlretrieve(url, dest)


def is_redirect(url):
    return urlparse.urlsplit(url).path == '/l.php'

def deredirect_link(url):
    return urlparse.parse_qs(urlparse.spliturl(url))['u'][0]    

def echoto(s,p):
    f=io.open(p,mode='w')
    f.write(s)
    f.flush()
    f.close()


#TODO:resumable sessions
def download_to_folder(browser,path):
    n=1
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    for page in conversation_pages(browser):
        for conversation in conversations_on_page(browser,page):
            name=conversation_name(browser,conversation)
            uid=conversation_id(conversation)
            convopath=os.path.join(path,str(n))
            try:
                os.mkdir(convopath)
            except FileExistsError:
                pass
            echoto(name,os.path.join(convopath,'name'))
            echoto(uid,os.path.join(convopath,'uid'))
            pdumphtml=os.path.join(convopath,'dump.html')
            fdumphtml=io.open(os.path.join(pdumphtml),mode='w')
            for convopage in pages_in_conversation(browser,conversation):
                fdumphtml.write(reverse_html_of_conversation_page(browser,convopage))
            fdumphtml.flush()
            fdumphtml.close()
            n+=1
