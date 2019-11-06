from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timedelta
import time
import pdb
def fetch_cor(cor_name='shopify+inc/1594805'):
    driver = webdriver.Chrome()
    driver.get('https://www.insidermonkey.com/login')
    time.sleep(3)
    driver.find_element_by_css_selector("#lgn-umail").send_keys("allen0909@hotmail.com")
    time.sleep(2)
    driver.find_element_by_css_selector("#lgn-upass").send_keys("Allen0909")
    time.sleep(3)
    driver.find_element_by_css_selector("#lgn-submit").click()
    time.sleep(7)
#抓取Hedge Fund
    def fetch_hedge(url,selector='hedge'):
        driver.get(url)
        time.sleep(5)
        def fetch_single(selector='hedge'):
            page = driver.page_source
            df_hedge = pd.read_html(page)[0]
            if selector == 'hedge':
                df_hedge = df_hedge[['Hedge Fund','Shares']]
            else:
                df_hedge = df_hedge[['Name','Shares']]
            return df_hedge
        trigger = True
        i = 1
        j = 1
        df_hedge_list = [fetch_single(selector)]
        while trigger:
            try:
                time.sleep(3)
                if selector == 'hedge':
                    driver.find_element_by_css_selector("#fund-holdings > div:nth-child({}) > div > div > ul > li:nth-child({}) > a".format(1,i+1)).click()
                else:
                    driver.find_element_by_css_selector("#small-fund-holdings > div:nth-child({}) > div > div > ul > li:nth-child({}) > a".format(1,i+1)).click()
                time.sleep(3)
                df_hedge_list.append(fetch_single(selector))
                i = 3
                j = j+1
            except:
                print("Thare are {} pages".format(j))
                trigger = False
        return pd.concat(df_hedge_list)
    
    cor_name = 'shopify+inc/1594805'
    #generate the dates
    end_date = pd.to_datetime(datetime.today())
    start_date = end_date - timedelta(days=365)
    date_list = pd.date_range(start_date,end_date,freq='Q').strftime('%Y-%m-%d').to_list()
    result_list = []
    for date in date_list:
        time.sleep(2)
        example = 'https://www.insidermonkey.com/insider-trading/company/{}/hedge-funds/#/ffp={}&fot=7&fso=1&sffp=&sfot=7&sfso=1'.format(cor_name,date)
        result = fetch_hedge(example)
        result_list.append(result)
    #fetch the inst data
    time.sleep(3)
    result_ins_list = []
    for date in date_list:
        time.sleep(2)
        example = 'https://www.insidermonkey.com/insider-trading/company/{}/institutional-investors/#/&sffp={}&sfot=7&sfso=1'.format(cor_name,date)
        result = fetch_hedge(example,'inst')
        result_ins_list.append(result)
    for df,date in zip(result_ins_list,date_list):
        df.to_csv('{}_ins.csv'.format(date))
    for df,date in zip(result_list,date_list):
        df.to_csv('{}.csv'.format(date))
    driver.quit()
if __name__ == '__main__':
    fetch_cor() 
    pdb.set_trace()
