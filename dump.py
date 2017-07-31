import selenium.webdriver
from getpass import getpass
from urllib import parse as urlparse

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
        threads=list(filter(lambda l: str(urlsplit(l).path).startswith('/messages/read'), links))
        if len(threads)==0:
            #no more threads
            return
        else:
            yield url
        pageNum+=1

def converstations_on_page(browser,url):
    browser.get(url)
    links=map(lambda e: e.get_attribute('href'),
              browser.find_elements_by_tag_name('a'))
    return filter(lambda l: str(urlsplit(l).path).startswith('/messages/read'), links)

def conversation_id(url):
    return urlparse.parse_qs(urlparse.urlsplit(url).query)['tid']

def conversation_name(browser,url):
    browser.get(url)
    return browser.title

#WARNING: This is in reverse chronological order
def pages_in_conversation(browser,url):
    browser.get(url)
    while True:
        older=browser.find_elements_by_id('see_older')
        if len(older)==0:
            break
        else:
            url=older[0].find_element_by_tag_name('a').get_attribute('href')
            yield url
            browser.get(url)

#reverses order and removes extra stuff
def filtered_html_of_conversation_page(browser,url):
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
