import bs4, requests, time
from selenium import webdriver
#from selenium.webdriver import Safari


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

#get article titles from search results
def techWTim():
    browser=webdriver.Safari()
    browser.get("https://www.techwithtim.net")
    searchbar=browser.find_element_by_css_selector("#search-2 > form > label > input")
    searchbar.click()
    searchbar.send_keys("test")
    searchbar.submit()
    time.sleep(5)
    try:
        main = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
        print(main.text)
        print('\n\n')
        articles =  main.find_elements_by_tag_name("article")
        for article in articles:
            header=article.find_element_by_class_name("entry-title")
            print(header.text)
    
    except:
        browser.quit()
    
    browser.quit()        

#click links 
def techWTim2():
    browser=webdriver.Safari()
    browser.get("https://www.techwithtim.net")

    link=browser.find_element_by_link_text("Python Programming")
    link.click()

    time.sleep(3)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
        )
        element.click()
        print('clicked')

        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "sow-button-19310003"))
        )
        element.click()
    except:
        browser.quit()

    time.sleep(5)
    print ("done")
    time.sleep(3)
    browser.quit()
    
#actionchains & automating cookie clicker
def techWTim3():
    browser=webdriver.Safari()
    browser.set_window_size(1024,768)
    browser.get("https://orteil.dashnet.org/cookieclicker/")



    
    browser.implicitly_wait(5)

    cookie=browser.find_element_by_id("bigCookie")
    numCookies=browser.find_element_by_id("cookies")
    items = [browser.find_element_by_id("productPrice" + str(i)) for i in range(1,-1,-1)]
    
    
    
    actions = ActionChains(browser)
    actions.click(cookie)


    for i in range(5000):
        actions.perform()
        count=int(numCookies.text.split(" ")[0])
        for item in items:
            value=int(item.text)
            if value<=count:
                upgrade_actions = ActionChains(browser)
                upgrade_actions.move_to_element(item)
                upgrade_actions.click()
                upgrade_actions.perform()
                
        
    
techWTim3()

def openCars():
    browser=webdriver.Safari()
    browser.get('https://www.truecar.com/used-cars-for-sale/listings/location-coppell-tx/')

    search = browser.find_element_by_css_selector('#main > main > div > div.sticky-top._90sllg > div:nth-child(2) > div > div > div:nth-child(2)')
    search.click()
    
    search = browser.find_element_by_css_selector('#main > main > div > div.sticky-top.sticky-wrapper-shadow._90sllg > div:nth-child(2) > div.padding-y-3.padding-x-3.w-100.border-top._1ingayf > div > div:nth-child(1) > label > div > div.range-slider.range-slider-hide-value.range-slider-double.range-slider-left-sticky-edge.range-slider-right-sticky-edge > div.d-flex.flex-column.padding-bottom-2_5 > div > label:nth-child(1) > div')
    search.click()
    print('whats the starting price: \n')
    sPrice=input()
    search.send_keys(sPrice)

    search= browser.find_element_by_css_selector('#main > main > div > div.sticky-top.sticky-wrapper-shadow._90sllg > div:nth-child(2) > div.padding-y-3.padding-x-3.w-100.border-top._1ingayf > div > div:nth-child(1) > label > div > div.range-slider.range-slider-hide-value.range-slider-double.range-slider-left-sticky-edge.range-slider-right-sticky-edge > div.d-flex.flex-column.padding-bottom-2_5 > div > label:nth-child(3)')
    search.click()
    print('whats the max price: \n')
    mPrice=input()
    search.clear()
    search.send_keys(mPrice)
    search.submit()



#goes on monster for dallas and lists all software jobs
def scrapeMonster():
    url='https://www.monster.com/jobs/search/?q=Software-Developer&where=Dallas'
    page=requests.get('https://www.monster.com/jobs/search/?q=Software-Developer&where=Dallas')
    print(page.raise_for_status)

    soup=bs4.BeautifulSoup(page.text, 'html.parser')
    results=soup.find(id='ResultsContainer')


    jobElems=results.find_all('section', class_ = 'card-content')

    for jobElem in jobElems:
        title=jobElem.find('h2', class_='title')
        company=jobElem.find('div',class_='company')
        location= jobElem.find('div', class_='location')
        if None in (title, company, location):
            continue
        print(title.text.strip())
        print(company.text.strip())
        print(location.text.strip())
        print('')


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

    
#scrapeMonster()












    
