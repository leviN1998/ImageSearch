from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome('C:/Users/levin/dev/Selenium/chromedriver.exe', options=chrome_options)

# open Website
driver.get('https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990')

# close new Tab with setting and switch to website again
window_name = driver.window_handles[0]
driver.switch_to.window(window_name=window_name)
driver.close()
window_name = driver.window_handles[0]
driver.switch_to.window(window_name=window_name)

# time.sleep(3)

# click cookies
driver.find_element_by_id('L2AGLb').click()

# time.sleep(3)

# insert query
aktion = driver.find_element_by_name('q')
aktion.send_keys("Tübingen")
aktion.submit()

time.sleep(0.5)

# scroll down
scroll_count = 5
for i in range(1,scroll_count+1):
    driver.execute_script("window.scrollTo(0,"  + str(i * 5000) + ");")
    time.sleep(3)

# click more images
driver.find_element_by_class_name('mye4qd').click()
time.sleep(3)

# scroll down
scroll_count = 6
for i in range(6,scroll_count+5+1):
    driver.execute_script("window.scrollTo(0,"  + str(i * 5000) + ");")
    time.sleep(3)

time.sleep(10)
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
print(usefull_images[300])
print(usefull_images[400])
print(usefull_images[410])
print(usefull_images[420])
print(usefull_images[430])



time.sleep(2)
driver.quit()