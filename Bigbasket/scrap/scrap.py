from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

import scrap.constants as const

class Scrap(webdriver.Chrome):
    
    def __init__(self, driver_path=r'C:\selenium-driver', teardown=False):
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver_path = driver_path
        self.teardown = teardown
        super(Scrap, self).__init__(options=options)
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


    def add_products():
        prduct_details =[]


    def land_first_page(self):
        self.get(const.BASE_URL)

    def click_category(self):
        select = self.find_element(By.CSS_SELECTOR, 'a[class="dropdown-toggle meganav-shop"]')
        select.click()
    
    def select_category(self):
        items = self.find_element(By.ID, 'navBarMegaNav')
        item = items.find_element(By.TAG_NAME, 'a')
        category = item.text
        item.click()
        return category
    

    def select_sub_category(self,category):
        sub_category = self.find_elements(By.CSS_SELECTOR, 'div[ng-if="subcategory.display_name"]')
        sub = sub_category[category].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'span')
        sub_category_name = sub.text.strip()
        sub.click()
        return sub_category_name
    
    
    def select_items(self,category,sub_category,product_no):
        product_details = []
        products = self.find_elements(By.TAG_NAME,'product-template')[:product_no]
        for product in products:
            data = {}
            price = product.find_element(By.CSS_SELECTOR, 'div[qa="price"]')
            data['Category'] =category
            data['Sub Category'] = sub_category
            data['SKU ID'] = ''
            data['Image'] = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
            data["Brand"] = product.find_element(By.TAG_NAME, 'h6').text
            data["SKU Name"] = product.find_element(By.CSS_SELECTOR, 'div[class="col-sm-12 col-xs-7 prod-name"]').find_element(By.TAG_NAME, 'a').text.strip()
            data["SKU Size"] = product.find_element(By.CSS_SELECTOR, 'span[data-bind="label"]').find_element(By.TAG_NAME, 'span').text
            data['MRP'] = price.find_element(By.CSS_SELECTOR, 'span[class="mp-price ng-scope"]').find_element(By.TAG_NAME, 'span').text
            data['SP'] = price.find_element(By.CSS_SELECTOR, 'span[class="discnt-price"]').text
            data['Link'] = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            data['Active'] = ''
            product_details.append(data)
        return product_details
    
    def go_back(self):
        self.back()

    
    def collect_data(self,cat,product):
        data=[]
        self.click_category()
        category = self.select_category()
        time.sleep(2)
        for i in range(cat):
            sub_cat = self.select_sub_category(i)
            cat_data = self.select_items(category,sub_cat,product)
            data = data+cat_data
            self.go_back()
        df = pd.DataFrame(data)
        df.to_csv('BigBasket.csv', index=False)
        return data
    
