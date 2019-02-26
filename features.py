#1 stands for legitimate

#-1 stands for phishing


import sys
import requests
from bs4 import BeautifulSoup
#import urllib, bs4, re


#import urllib.request
# from selenium import webdriver
#import urllib2, httplib
# import OpenSSL, sslbvnb
# import requests
from googlesearch import search

#from google import google
import whois
from datetime import datetime
import time



import socket
proxyDict = { 
          'http'  : None, 
          'https' : None
        }



def ip_address(url):
    match=re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  #IPv4
                    '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  #IPv4 in hexadecimal
                    '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)     #Ipv6
    if match:
        
        return -1
    else:
        
        return 1

def URL_length(url):
    if len(url)<54:
        return 1
    if len(url)>=54 and len(url)<=75:
        return 0
    else:
        return -1

def short_url(url):
    result=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
    if result:

        return -1
    else:
        return 1

def at_symbol(url):

    result=re.search('@',url)
    if result:
        return -1
    else:
        return 1

def double_slash(url):

    
    list=[x.start(0) for x in re.finditer('//', url)]

    
    if list[len(list)-1]>6:
        return -1
    else:
        return 1
    
    
def pre_suf(domain):
    result=re.search('-',domain)
    if result:
        return -1
    else:
        return 1

def sub_domain(url):

    if ip_address(url)==-1:
        result=re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)
        i=result.end(0)
        url=url[i:]
    list=[x.start(0) for x in re.finditer('\.',url)]
    if len(list)<=3:
        return 1
    elif len(list)==4:
        return 0
    else:
        return -1





def domain_registration_length(domain):
    expiration_date = domain.expiration_date
    #print (expiration_date)
    if expiration_date is None:
      return -1

    today = time.strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    #print (today)
    try:
        registration_length = abs((expiration_date - today).days)
    except:
        registration_length = abs((expiration_date[0] - today).days)
    
    #print ("re"+str(registration_length))
    #print (registration_length)
    if registration_length  <= 365:
        return -1
    else:
        return 1
    
    return 1
    
def favicon(url, soup, domain):
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                return 1
            else:
                return -1
    return 1

def https(url):
    result=re.search('https://|http://',url)

    if result.start(0)==0:
        url=url[result.end(0):]
    
    result=re.search('http|https',url)
    if result:
        return -1
    else:
        return 1

def request_url(url, soup, domain):
   i = 0
   success = 0
   for img in soup.find_all('img', src= True):
      dots= [x.start(0) for x in re.finditer('\.', img['src'])]
      if url in img['src'] or domain in img['src'] or len(dots)==1:
         success = success + 1
      i=i+1

   for audio in soup.find_all('audio', src= True):
      dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
      if url in audio['src'] or domain in audio['src'] or len(dots)==1:
         success = success + 1
      i=i+1

   for embed in soup.find_all('embed', src= True):
      dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
      if url in embed['src'] or domain in embed['src'] or len(dots)==1:
         success = success + 1
      i=i+1

   for iframe in soup.find_all('iframe', src= True):
      dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
      if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
         success = success + 1
      i=i+1
   success=i-success
   #print ("is"+str(success)+" "+str(i))
   try:
      percentage = success/float(i) * 100
   except:
       return 1
   #print(percentage)
   if percentage < 22.0 :
      return 1
   elif((percentage >= 22.0) and (percentage < 61.0)) :
      return 0
   else :
      return -1

def anchor(url, soup, domain):
    i = 0
    unsafe=0
    for a in soup.find_all('a', href=True):
   
        
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
        #print (a['href'])
    #print (str(i)+" "+str(unsafe))
    try:
        percentage = (unsafe / float(i)) * 100
    except:
        return 1    
    #print (percentage)
    if percentage < 31.0:
        return 1
        # return percentage
    elif ((percentage >= 31.0) and (percentage < 98.0)):
        return 0
    else:
        return -1


def link_tag(url, soup, domain):
   i=0
   success =0
   for link in soup.find_all('link', href= True):
      dots=[x.start(0) for x in re.finditer('\.',link['href'])]
      if url in link['href'] or domain in link['href'] or len(dots)==1:
         success = success + 1
      i=i+1

   for script in soup.find_all('script', src= True):
      dots=[x.start(0) for x in re.finditer('\.',script['src'])]
      if url in script['src'] or domain in script['src'] or len(dots)==1 :
         success = success + 1
      i=i+1
   success=i-success
   try:
       percentage = success / float(i) * 100
   except:
       return 1
   #print(str(i)+" "+str(success)+" "+str(percentage))

   if percentage < 17.0 :
      return 1
   elif((percentage >= 17.0) and (percentage < 81.0)) :
      return 0
   else :
      return -1


def sfh(url, soup, domain):
   for form in soup.find_all('form', action= True):
      if form['action'] =="" or form['action'] == "about:blank" :
         return -1
      elif url not in form['action'] and domain not in form['action']:
          return 0
      else:
            return 1
   return 1


def email(soup):
   for form in soup.find_all('form', action= True):
      if "mailto:" in form['action'] :
         return -1
      else:
          return 1
   return 1

def abnormal_url(domain,url):
    #print (domain.domain_name)
    
    hostname=domain.domain_name[0].lower()
    #print(hostname)
    match=re.search(hostname,url)
    if match:
        return 1
    else:
        return -1
    



def iframe(soup):
    for iframe in soup.find_all('iframe', width=True, height=True, frameBorder=True):
        if iframe['width']=="0" and iframe['height']=="0" and iframe['frameBorder']=="0":
            return -1
        
    return 1


def age_of_domain(domain):
    creation_date = domain.creation_date
    if creation_date is None:
      return -1

    expiration_date = domain.expiration_date
    if expiration_date is None:
      return -1
    try:
        ageofdomain = abs((expiration_date - creation_date).days)
    except:
        ageofdomain = abs((expiration_date[0] - creation_date[0]).days)

    #ageofdomain = abs((expiration_date - creation_date).days)
    #print (ageofdomain)
    if ageofdomain / 30 < 6:
        return -1
    else:
        return 1

def report(url,hostname):
    result=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address=socket.gethostbyname(hostname)
    except:
        print ('Error')
    ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                       '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                       '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                       '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                       '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                       '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
    if result:
        return -1
    elif ip_match:
        return -1
    else:
        return 1

     
  

    
    




def redirect(url):

  count=0
  httplib.HTTPConnection.debuglevel = 1
  '''
  while True:
    
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    f=opener.open(request)
    
    
    url = f.url
    count += 1
    if count>=2:
      break
    url = f.url
    count += 1
  '''
  f = requests.get(url, proxies=proxies)
  for resp in f.history:
    count+=1
  if count<=1:
    return 1
  elif count>=2 and count<4:
    return 0
  else:
    return -1 




def main(url):
    
    page = requests.get(url)
    print ("Webpage request "+str(page.status_code))

    
    with open('markup.txt', 'r') as file:
        soup_string=file.read()

    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    array=[]

    hostname = url
    h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
    z = int(len(h))
    if z != 0:
        y = h[0][1]
        hostname = hostname[y:]
        h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
        z = int(len(h))
        if z != 0:
    
            hostname = hostname[:h[0][0]]
    
    
    #print (hostname)
    array.append(ip_address(url))
    #print (url_length(url))
    array.append(URL_length(url))
    array.append(short_url(url))
    array.append(at_symbol(url))
    array.append(double_slash(url))
    
    array.append(pre_suf(hostname))
    array.append(sub_domain(url))
    

    dns=1
    try:
        domain = whois.whois(hostname)
    except:
        dns=-1
    print ("Whois Data fetching status: "+str(dns))
    #print (domain)
    if dns==-1:
        array.append(-1)
    else:
        array.append(domain_registration_length(domain))

    array.append(favicon(url,soup, hostname))
    array.append(https(url))
    array.append(request_url(url, soup, hostname))
    array.append(anchor(url, soup, hostname))
    array.append(link_tag(url,soup, hostname))
    array.append(sfh(url,soup, hostname))
    
    array.append(email(soup))
    
    
    if dns == -1:
        array.append(-1)
    else:
        array.append(abnormal_url(domain,url))
    
    
    array.append(iframe(soup))
    #print (age_of_domain(domain))
    
    if dns == -1:
        array.append(-1)
    else:
        array.append(age_of_domain(domain))
    
    array.append(dns)
    
    
    array.append(report(url,hostname))
    
   
    return array

if __name__ == "__main__":
    main()
