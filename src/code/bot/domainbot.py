import os, sys
from urllib.parse import urlparse, urljoin
import requests
import re
from bs4 import BeautifulSoup
import pickle

headers = {'user-agent': 'simpleBot description/keywords_landing_page_no_crawler code/0.0.1'}

#functions

def custom_robotparser(page):
    '''
    simple bot parser
    '''
    bot = requests.get(page)
    if bot.status_code == 404:
        True
    #parsing the response (bot)
    ck = [(a.split(':')[0], a.split(':')[1][1:]) for a in bot.content.decode('utf8').split('\n')[:-1] if a.find(':')>-1]
    for pair in ck:
        if pair[0] == 'Disallow':
            if pair[1] == '\\':
                return False
    return True
                

def botvisitor(URL_BASE_1, httpZsecurity):
    if urlparse(URL_BASE_1)[0] == '':
        URL_BASE_2 = httpZsecurity+URL_BASE_1
    try:
        print(urljoin(URL_BASE_2,'/robots.txt'))
        if custom_robotparser(urljoin(URL_BASE_2,'/robots.txt')) == True:
            print('robot parser successful for ', URL_BASE_2, '\n')
            treatedZdata[URL_BASE_1]['minsecurity'] = httpZsecurity
            treatedZdata[URL_BASE_1]['title'], treatedZdata[URL_BASE_1]['description'], treatedZdata[URL_BASE_1]['keywords'], treatedZdata[URL_BASE_1]['htext'] = finding_tags_test(URL_BASE_2)
            treatedZdata[URL_BASE_1]['crawlstatus'] = 'ok_crawl'
        else:
            print('crawling not allowed for ', URL_BASE_2, '\n')
            treatedZdata[URL_BASE_1]['crawlstatus'] = 'no_crawl'            
    except:
        print('robot parser failed for ', URL_BASE_2, '\n')
        treatedZdata[URL_BASE_1]['crawlstatus'] = 'err_crawl'  
    

def finding_tags(page):
    '''
    if crawling allowed, find main page and look for texts in tags:
    --- description
    --- title
    --- keywords
    '''

    try:
        r = requests.get(page, headers=headers)
    except:
        print('error reaching the page ', x, '; code status ', r.status_code)
        return ['errorreachingpage']*4
    soup = BeautifulSoup(r.content)
    ks = {'description':'noinformationfound', 'keywords': 'noinformationfound', 'title':'noinformationfound', 'htext':'noinformationfound'}
    t = 0
    try:
        #title
        ks['title'] = t = soup.title.get_text().lower()
        
        
        allmeta = soup.find_all("meta")
        
        #description
        for m1 in allmeta:
            if m1.attrs.get('name'):
                if m1.attrs.get('name').lower() == 'description':
                    ks['description'] = m1.attrs.get('content').lower()
                    print(ks['description'])
                    break
        
        #keywords
        for m2 in allmeta:
            if m2.attrs.get('name'):                
                if m2.attrs.get('name').lower() == 'keywords':
                    ks['keywords'] = m2.attrs.get('content').lower()
                    print(ks['keywords'])
                    break
        
        #first paragraph, first h1, first h2
        fp = soup.find_all("p")
        if fp:
            if ks['htext'] == 'noinformationfound':
                ks['htext'] = fp[0].text + ' '      
        
        fh1 = soup.find_all("h1")
        if fh1:
            if ks['htext'] == 'noinformationfound':
                ks['htext'] = fh1[0].text + ' '
            else:
                ks['htext'] = ks['htext'] + fh1[0].text + ' '        
        
        fh2 = soup.find_all("h2")
        if fh2:
            if ks['htext'] == 'noinformationfound':
                ks['htext'] = fh2[0].text + ' '
            else:
                ks['htext'] = ks['htext'] + fh2[0].text + ' '  

    except:
        #just wrap if an error occurred, not matter at which point
        print('error when finding some information for ', x)
    
    finally:
        return ks['title'],ks['description'],ks['keywords'],ks['htext']
        #return desc_and_kw


def bot(data, filename):
    '''
    after research, I found that what I originally did was ok:
    https://stackoverflow.com/questions/23764639/python-detect-is-a-url-needs-to-be-https-vs-http
    
    urls will be pre-selected to reduce the complexity; they will be mostly javascript-related (see given regex patterns to get an idea)
    '''
    
    directory = "/home/ec/Documents/MainComp_Programming/FreeCodeCamp/data_analysis/1_archive"

    treatedZdata = {}
    #OJO with first pattern!!!! it was preventing further readings!! too strict
    pattern01 = re.compile(r'html|css|javascript|js|node\.?js?|angular|react\.?js?|bootstrap|jquery', flags=re.IGNORECASE)
    pattern02 = re.compile(r'(\b$|\\$|(([a-z]+\.)?(google|freecatphotoapp|twitch|gitter|codepen|youtube|github|freecodecamp|massdrop-s3\.imgix|imgur|walmart|googleusercontent|youtu|s-media-cache-ak0|pinimg|quisk|quisk|flickr)(\.[a-z]+)))', flags=re.IGNORECASE)
    pattern03 = re.compile(r'herokuapp|postimg|prnt|kym-cdn|imgflip|instagram|twimg|gyazo|bp\.blogspot|@', flags=re.IGNORECASE)
    pattern04 = re.compile(r'meme|\.(gif|jpeg|jpg|png)$',flags=re.IGNORECASE)
    
    count0 = 0
           
    for URL_BASE in list(data.keys()):
        
        for elem in data[URL_BASE]:
            url = elem['url1']
            params = elem['params']
            
            print(url)
            
            ##domains that I don't want (OJO: ALWAYS compiled as (xxx.)?DOMAINNAME(.xxx)) OR words that I don't want in the domain
            
            if re.match(pattern02, URL_BASE) != None or re.search(pattern03, URL_BASE) != None:
                continue
            
            ##extensions that either don't want or should be conditioned
            if re.search(pattern04, url):
                continue
            if url.find(".js") > -1:
                if url.replace(".js", "").find("js") == -1:
                    continue
            if url.find(".html") > -1:
                if url.replace(".html", "").find("html") == -1:
                    continue
            
            ##urls with a good domain but an unaccepted param
            if params in ("/fcc-relaxing-cat", "/t/free-code-camp-official-chat-rooms/19390", "/t/free-code-camp-official-chat-rooms", "/t/free-code-camp-brownie-points/18380", "/t/markdown-code-formatting/18391"):
                continue
    

            if re.search(pattern01, url):
                if URL_BASE not in list(treatedZdata.keys()):
                    treatedZdata[URL_BASE] = {}
                    treatedZdata[URL_BASE]['minsecurity'] = None
                    treatedZdata[URL_BASE]['crawlstatus'] = None
                    treatedZdata[URL_BASE]['title'] = None
                    treatedZdata[URL_BASE]['description'] = None
                    treatedZdata[URL_BASE]['keywords'] = None
                    treatedZdata[URL_BASE]['htext'] = None
                    treatedZdata[URL_BASE]['params'] = set()
                treatedZdata[URL_BASE]['params'].update([params])


  
    for URL_BASE_1 in list(treatedZdata.keys()):
        botvisitor(URL_BASE_1, 'https://')
    
    for URL_BASE_1 in list(treatedZdata.keys()):
        if treatedZdata[URL_BASE_1]['crawlstatus'] == 'err_crawl': ##TEMPORARY LINE!!!
            botvisitor(URL_BASE_1, 'http://')

    pickle.dump(d, open(directory+'/'+filename+'_fulldata_links.pkl', 'wb')) #dictionary
    pickle.dump(treatedZdata, open(directory+'/'+filename+'_treateddata_links.pkl','wb')) #dictionary