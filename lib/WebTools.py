from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time

from PIL import Image
import io
import os

class WebTools():
    def __init__(self):
        self.options = Options()
        self.options.add_argument('-headless')

    def screenshot_by_id(self, web_link, save_path, element_id):
        with webdriver.Firefox(options=self.options) as driver:
            driver.get(web_link)
            image_binary = driver.find_element(By.ID, element_id).screenshot_as_png 
            img = Image.open(io.BytesIO(image_binary))
            img.save(save_path)
#        # check if image is saved:
#        for i in range(0, 10):
#            time.sleep(1)
#            if os.path.isfile(save_path):
#                break          
#        return save_path