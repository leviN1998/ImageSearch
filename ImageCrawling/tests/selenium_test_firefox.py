from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time

options = Options()
options.add_argument("--headless")

current_pwd = os.getcwd()
driver_path = current_pwd + "geckodriver.exe"
driver = webdriver.Firefox(options=options)

# open Website
driver.get('https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990')

time.sleep(2)

# click cookies
driver.find_element_by_id('L2AGLb').click()

time.sleep(2)

# insert query
aktion = driver.find_element_by_name('q')
aktion.send_keys("Tübingen")
aktion.submit()

time.sleep(2)


images = driver.find_elements_by_tag_name('img')
total = len(images)
data = 0
src_none = 0
usefull_images = []
print(len(images))
for image in images:
    src = image.get_attribute('src')
    if src == None:
        src_none += 1
    elif src[0] == 'd':
        data += 1
    else:
        usefull_images.append(image.get_attribute('src'))

print("Total: ", total, "    Data: ", data, "    Not None: ", total - (src_none + data), "    None: ", src_none)