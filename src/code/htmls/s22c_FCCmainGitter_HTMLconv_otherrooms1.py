#!/usr/bin/env python3
#from chatroom_analysis/cr_analysis.py
import os, sys
import pickle
import operator, collections
import nltk
import re
nltk.data.path.append('/home/ec/anaconda3/nltk_data')

usual_stopwords = nltk.corpus.stopwords.words('english')
other_words = ["re", "fm", "tv", "la", "al", "ben", "aq", "ca", "can", "can'", "can't", "cant", "&"]
punctuation = ["\\","/", "|","(",")",".",",",":","=","{","}","==", "===","[","]","+","++","-","--","_","<",">","'","''","``",'"',"!","!=","?",";"]
wtbr = usual_stopwords + other_words + punctuation

directory = "/home/ec/Documents/MainComp_Programming/FreeCodeCamp/data_analysis/1_archive"

def getting_treated_links(dd1, filename):
    data = {}
    
    crawled = pickle.load(open(directory+'/'+filename+'_treateddata_links.pkl','br'))
    for k1 in list(crawled.keys()):
        if k1 in list(dd1.keys()):
            data[k1] = {}
            data[k1]['count1'] = dd1[k1]['count1']
            data[k1]['count2'] = dd1[k1]['count2']
            data[k1]['repos'] = dd1[k1]['repos']
            data[k1]['last'] = dd1[k1]['last']
            data[k1]['params'] = list(dd1[k1]['repos'].keys())
            if crawled[k1]['title'] == -1 or crawled[k1]['title'] == 0 or crawled[k1]['title'] == None:
                data[k1]['title'] = ''
            else:
                data[k1]['title'] = crawled[k1]['title']
            if crawled[k1]['description'] == -1 or crawled[k1]['description'] == 0 or crawled[k1]['description'] == None:
                data[k1]['description'] = ''
            else:
                data[k1]['description'] = crawled[k1]['description']
            if crawled[k1]['keywords'] == -1 or crawled[k1]['keywords'] == 0 or crawled[k1]['keywords'] == None:
                data[k1]['keywords'] = ''
            else:
                data[k1]['keywords'] = crawled[k1]['keywords']
            if crawled[k1]['htext'] == -1 or crawled[k1]['htext'] == 0 or crawled[k1]['htext'] == None:
                data[k1]['htext'] = ''
            else:
                data[k1]['htext'] = crawled[k1]['htext']
    return data


def to_html_reference(d1, l = 2, domain = 'www.w3schools.com'): #FOR d1 !!!
    html = ''
    for elem in d1[domain][:l]:
        #print(elem)
        text = '<li>'+elem['text']+' (POSTER: '+elem['user']+')</li>'
        #hardcoded!!
        if text.find(domain) > -1:
            #print(text)
            for url in elem['urls']:
                #print(url)
                if url['url'].find(domain) > -1:
                    text = text.replace(url['url'], "<a href='#'><span style='font-size:120%;'>"+url['url']+"</span></a>")
                    html = html + text
    return html


def to_html_ranking(dd1, dd1_treated, bow): #FOR dd1 !!!
    html = ''
    bow = bow()
    lwords = []
    #for k in sorted(dd1_treated, key=lambda k: dd1[k]['last'].timestamp(), reverse=True):
    pattern01 = re.compile(r'[^a-z0-9]', flags=re.IGNORECASE)
    pattern02 = re.compile(r'\d+', flags=re.IGNORECASE)
    pattern03 = re.compile(r'\w$', flags=re.IGNORECASE)
    
    for k in sorted(dd1_treated, key=lambda k: 100*dd1_treated[k]['count2']/(11*dd1_treated[k]['count1']), reverse=True):
        if k == '':
            continue

       
        kwsset = set()
        
       
        count = 0
        if dd1_treated[k]['description'] != '' or dd1_treated[k]['description'] != 'noinformationfound' or dd1_treated[k]['description'] != 'errorreachingpage':
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['description'].lower()).split(' ')) 
            count += 1
        if dd1_treated[k]['keywords'] == '' or dd1_treated[k]['keywords'] != 'noinformationfound' or dd1_treated[k]['keywords'] != 'errorreachingpage':
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['keywords'].lower()).split(' '))
            count += 1
        if dd1_treated[k]['title'] == '' or dd1_treated[k]['title'] != 'noinformationfound' or dd1_treated[k]['title'] != 'errorreachingpage':          
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['title'].lower()).split(' '))
            count += 1
        if dd1_treated[k]['htext'] == '' or dd1_treated[k]['htext'] != 'noinformationfound' or dd1_treated[k]['htext'] != 'errorreachingpage':          
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['htext'].lower()).split(' '))
            count += 1
        
        if count == 0:
            for p in dd1_treated[k]['params']:
                kwsset.update(re.sub(pattern01, ' ', p.lower()).split(' '))
      
       
        for e in kwsset:
            #assert type(e).__name__ == str, type(e)
            if (e != '' or e != ' ') and not re.match(pattern02, e) and e not in wtbr:
                if e in ['rants', 'rant']:
                    e = 'blog'
                lwords.append(e)
        
    lwords = dict(sorted(collections.Counter(lwords).items(), key=lambda x:x[1], reverse=True))
    
    
    
    for kk in lwords.keys():
        if lwords[kk] <= 1:
            if kk in list(bow.keys()):
                lwords[kk] = lwords[kk] + 10
        else:
             if kk in list(bow.keys()):
                lwords[kk] = lwords[kk] + 10           
    
    lwords = dict(filter(lambda x: x[1] > 1, lwords.items()))

    #for k in sorted(dd1_treated, key=lambda k: 100*dd1_treated[k]['count2']/(11*dd1_treated[k]['count1']), reverse=True):
    starpart = len(dd1_treated)
    counter = 0
    for k in sorted(dd1_treated, key=lambda k: (100*dd1_treated[k]['count2']/11, dd1_treated[k]['count1']), reverse=True):
        if k == '':
            continue
        
        kwsset = set()
        
        
        
        
       
        count = 0
        if dd1_treated[k]['description'] != '' and (dd1_treated[k]['description'] != 'noinformationfound' or dd1_treated[k]['description'] != 'errorreachingpage'):
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['description'].lower()).split(' ')) 
            count += 1
        if dd1_treated[k]['keywords'] == '' and (dd1_treated[k]['keywords'] != 'noinformationfound' or dd1_treated[k]['keywords'] != 'errorreachingpage'):
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['keywords'].lower()).split(' '))
            count += 1
        if dd1_treated[k]['title'] == '' and (dd1_treated[k]['title'] != 'noinformationfound' or dd1_treated[k]['title'] != 'errorreachingpage'):          
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['title'].lower()).split(' '))
            count += 1
        if dd1_treated[k]['htext'] == '' and (dd1_treated[k]['htext'] != 'noinformationfound' or dd1_treated[k]['htext'] != 'errorreachingpage'):          
            kwsset.update(re.sub(pattern01, ' ', dd1_treated[k]['htext'].lower()).split(' '))
            count += 1
        
        # if count == 0:
        #     for p in dd1_treated[k]['params']:
        #         kwsset.update(re.sub(pattern01, ' ', p.lower()).split(' '))
        # 
        for p in dd1_treated[k]['params']:
            kwsset.update(re.sub(pattern01, ' ', p.lower()).split(' '))
        
        kwsset.update(k.split('.'))
        
        
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        
        redundant = ['web', 'development', 'developer', 'javascript', 'js', 'programming', 'code', 'new', 'things', 'started', 'powerful', 'source', 'get', 'use', 'like', 'using', 'used', 'us', 'com', 'world', 'latest', 'open']
        
        pairkv = []
        for kst in kwsset:
            if kst in list(lwords.keys()):
                pairkv.append((kst,lwords[kst]))
        
        pairkv = sorted(pairkv, key=lambda x:x[1], reverse=True)
        
        #kws = ', '.join(w for w in list(kwsset) if w in list(lwords.keys()) and w not in ['errorreachingpage', 'noinformationfound', ''] and w not in months and not re.match(pattern03, w)).strip()
        
        
        kws = ', '.join([w for w, i in pairkv if w not in ['errorreachingpage', 'noinformationfound', ''] and w not in months and w not in redundant and not re.match(pattern03, w)]).strip()

        pairkv2 = [(w , i) for w, i in pairkv if w not in ['errorreachingpage', 'noinformationfound', ''] and w not in months and w not in redundant and not re.match(pattern03, w)]
        
        
        
        if len(kws) != 0 and kws[0] == ',':
            kws = kws[2:].strip()
        
       #http://www.regular-expressions.info/backref2.html
        areas = ['shop|commerce', 'community|support|people|forum', '(text )?editor|interpreter|repl', 'learn|tutorial|course|training| tips|example', 'blog|media|news|articl|content|post|journal', 'api|package|framework|librar|stack|licens|addon|app', 'design|galler|template|theme', 'cloud|platform|service', 'docs',]
        
        area = '---'
        
        if re.search(re.compile(areas[0]),kws):
            area = areas[0]
        elif re.search(re.compile(areas[1]),kws):
            area = areas[1]
        elif re.search(re.compile(areas[2]),kws):
            area = areas[2]
        elif re.search(re.compile(areas[3]),kws):
            area = areas[3]
        elif re.search(re.compile(areas[4]),kws):
            area = areas[4]
        elif re.search(re.compile(areas[5]),kws):
            area = areas[5]
        elif re.search(re.compile(areas[6]),kws):
            area = areas[6]
        elif re.search(re.compile(areas[7]),kws):
            area = areas[7]
        elif re.search(re.compile(areas[8]),kws):
            area = areas[8]
        

        if kws.split(',')[0] == 'learn' and 'community|support|people|forum':
            area = 'learn|tutorial|course|training| tips|example'

        if kws.split(',')[0] == 'news' and 'community|support|people|forum':
            area = 'blog|media|news|articl|content|post|journal'
        
        if area == 'community|support|people|forum' and k.split('.')[-2][-2:] == 'js':
            area = 'api|package|framework|librar|stack|licens|addon|app'

         
        kws = ', '.join(["<span>"+w+"</span>" for w, i in pairkv if w not in ['errorreachingpage', 'noinformationfound', ''] and w not in months and w not in redundant and not re.match(pattern03, w) and i > 18]).strip()
        
         
        if dd1_treated[k]['description'] != '' and dd1_treated[k]['description'] != 'noinformationfound' and dd1_treated[k]['description'] != 'errorreachingpage':
        #     #print(k, dd1_treated[k]['description'], len(dd1_treated[k]['description']))
            if re.search(re.compile('cloud'),dd1_treated[k]['description']) and re.search(re.compile('platform|service|computing'),dd1_treated[k]['description']):
                area = 'cloud|platform|service'
            if re.search(re.compile('on?(-|\s)?demand|business|compan(y|ies)|enterprise'),dd1_treated[k]['description']) and not re.search(re.compile('learn|tutorial|course|training|tips|example'),dd1_treated[k]['description']):
                area = 'on?(-|\s)?demand|business|compan(y|ies)|enterprise'  
                
            kws = "<span style='font-size:60%;'>"+str(dd1_treated[k]['description'])+"</span>"

        #print(pairkv2[0][0], pairkv2[1][0])
        if area.find('learn') != -1 and k.split('.')[-2][-2:] == 'js' and (pairkv2[0][0] == 'api' or pairkv2[1][0] == 'api'):
            area = 'api|package|framework|librar|stack|licens|addon|app'

        if area.find('docs') != -1 and k.split('.')[-2][-2:] == 'js':
            area = 'api|package|framework|librar|stack|licens|addon|app'

        # if k =='mongoosejs.com':
        #     print(area.find('learn'), k.split('.')[-2][-2:] == 'js', pairkv2[0][0], pairkv2[1][0] )
        #     break
        
        if 'api' in k.split('.'):
            area = 'api|package|framework|librar|stack|licens|addon|app'
        
        if 'blog' in k.split('.') or 'weblog' in k.split('.'):
            area = 'blog|media|news|articl|content|post|journal'    
        
        if {'dev', 'devs', 'developers', 'developer', 'docs'}.intersection(set(k.split('.'))):
            area = 'manual|guide|docs'

            
        #html = html + "<tr><td><a href='reference.html'>"+k+"</a></td><td>"+kws+"</td><td>"+"{0:.2f}".format(100*dd1_treated[k]['count2']/(11*dd1_treated[k]['count1']))+"</td></tr>"
        #html = html + "<tr><td><a href='reference.html'>"+k+"</a></td><td>"+kws[1:-2]+"</td><td>"+"{0:.2f}, {1}, {2:.2f}".format(rr, dd1_treated[k]['count1'] ,100*dd1_treated[k]['count2']/(11*dd1_treated[k]['count1']))+"</td></tr>"
        #html = html + "<tr><td><a href='reference.html'>"+k+"</a></td><td>"+kws[1:-2]+"</td><td>"+"{:.2f}".format(rr)+"</td></tr>"
        html = html + "<tr><td><a href='#'>"+k+"</a></td><td style='font-size:110%;color:#3A4462;'>"+kws[:]+"</td><td style='font-size:110%;color:#3A4462;'>"+area+"</td><td style='font-size:75%;'><button type='button' class='btn btn-primary'>more</button></td></tr>"
        counter += 1
        #if counter == 10:
        #    break
    #print(len(bow))
    return html, lwords

def mainhtmlcode(d1, dd1, filename):
    dd1_treated = getting_treated_links(dd1, filename)
    html, lwords = to_html_ranking(dd1, dd1_treated, bow)
    print(html)
    with open(directory+'/'+filename+'_links.html','w') as f:
        f.write(html)
        
    #html = to_html_reference(d1)
    #print(html)
    
    #return lwords
    return None

