import selenium.webdriver
from getpass import getpass
from urllib.parse import urlsplit

fburl = 'https://m.facebook.com'
browser = selenium.webdriver.Firefox()

######
#login
browser.get(fburl)
try:
    browser.execute_script('alert("Log in manually pls, then press ENTER on the command line.")')
except:
    pass
input()
# this is because we don't wanna deal
# with all the crap FB can throw up
# like this one tap login thing

###########################
# let's start the fun stuff
#TODO: go to next page of thread list
#TODO: detect last page
browser.get(fburl+'/messages')
pageNum=0
while True:
    links=map(lambda e: e.get_attribute('href'),
              browser.find_elements_by_tag_name('a'))
    threads=list(filter(lambda l: urlsplit(l).path.startswith('/messages/read'), links))
    if len(threads)==0:
        #no more threads
        break
    for thread in threads:
        #this is also paginated
        browser.get(thread)
        #TODO yield or stg here?
        while True:
            print(browser.find_element_by_id('messageGroup')
                  .get_attribute('innerHTML'))
            older=browser.find_elements_by_id('see_older')
            if len(older)==0:
                break
            else:
                older[0].find_element_by_tag_name('a').click()
        
    pageNum+=1
    
