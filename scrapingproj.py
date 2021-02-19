import bs4, requests, time
from selenium import webdriver
#from selenium.webdriver import Safari
#media bias scraper

def get_agreeance_text(ratio):
    if ratio > 3: return "absolutely agrees"
    elif 2 < ratio <= 3: return "strongly agrees"
    elif 1.5 < ratio <= 2: return "agrees"
    elif 1 < ratio <= 1.5: return "somewhat agrees"
    elif ratio == 1: return "neutral"
    elif 0.67 < ratio < 1: return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67: return "disagrees"
    elif 0.33 < ratio <= 0.5: return "strongly disagrees"
    elif ratio <= 0.33: return "absolutely disagrees"
    else: return None


def mediaBiasPrac():
    url='https://www.allsides.com/media-bias/media-bias-ratings'
    site=requests.get(url)
    print(site.raise_for_status())
    soup=bs4.BeautifulSoup(site.content,'html.parser')

    rows=soup.select('tbody tr')
    row=rows[0]
    name=row.select_one('.source-title').text.strip()
    print(name)

    allsides_page = row.select_one('.source-title a')['href']
    allsides_page= 'https://www.allsides.com' + allsides_page
    print(allsides_page)

    bias=row.select_one('.views-field-field-bias-image a')['href']
    bias=bias.split('/')[-1]
    print(bias)

    agree = row.select_one('.agree').text
    agree=int(agree)

    disagree=row.select_one('.disagree').text
    disagree=int(disagree)

    agree_ratio=agree/disagree

    print(f"Agree: {agree}, Disagree: {disagree}, Ratio {agree_ratio:.2f}")

    print(get_agreeance_text(agree_ratio))


    data = []

    for row in rows:
        d=dict()

        d['name']=row.select_one('.source-title').text.strip()
        d['allsides_page']='https://www.allsides.com' + row.select_one('.source-title a')['href']
        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
        d['agree']=int(row.select_one('.agree').text)
        d['disagree']=int(row.select_one('.disagree').text)
        d['agree_ratio']= d['agree'] / d['disagree']
        d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

        data.append(d)
        

    print((data[0])['agree'])


def mediaBias():
    import json
    from time import sleep
    pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
    ]
    data = []

    for page in pages:
        site=requests.get(page)
        soup=bs4.BeautifulSoup(site.content,'html.parser')
        rows = soup.select('tbody tr')
        
        for row in rows:
            d=dict()
            print('step')
            try:
              d['name']=row.select_one('.source-title').text.strip()
            except AttributeError:
                pass
            try:
              d['allsides_page']='https://www.allsides.com' + row.select_one('.source-title a')['href']
            except TypeError:
                pass
            try:
               d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
            except TypeError:
                pass
            try:
              d['agree']=int(row.select_one('.agree').text)
            except AttributeError:
                pass
            try:
              d['disagree']=int(row.select_one('.disagree').text)
            except AttributeError:
                pass
            try:
              d['agree_ratio']= d['agree'] / d['disagree']
            except KeyError:
                pass
            try:
              d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])
            except KeyError:
                pass

            data.append(d)
            
        
    from copy import deepcopy
    from tqdm import tqdm_notebook

    for d in tdqm.notebook.tdqm(data):
        r = requests.get(d['allsides_page'])
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
            
        try:
            website = soup.select_one('.www')['href']
            d['website'] = website
        except TypeError:
            pass
            
        sleep(10)


    with open('allsides.json', 'w') as f:
        json.dump(data, f)
    with open('allsides.json', 'r') as f:
        data = json.load(f)


    abs_agree = [d for d in data if d['agreeance_text'] == 'absolutely agrees']

    print(f"{'Outlet':<20} {'Bias':<20}")
    print("-" * 30)

    for d in abs_agree:
        print(f"{d['name']:<20} {d['bias']:<20}")

    













    
