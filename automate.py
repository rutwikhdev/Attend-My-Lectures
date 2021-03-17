from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import time
import yaml


# 1 to allow, 2 to block
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1 
})

with open('creds.yaml', 'r') as fp:
	creds = yaml.safe_load(fp)

with open('tt.yaml', 'r') as fp:
	time_table = yaml.safe_load(fp)


# Get current time
now = datetime.datetime.now()
weekday = now.strftime('%A')


# Get lecture time
for lec in time_table[weekday]:
    h, m, s = lec['Time'].split(':')
    lec_time = datetime.time(int(h), int(m), int(s))
    cur_time = datetime.datetime.now().time()

    if cur_time >= lec_time:
        lec_code = lec['Code']

print(creds['meet_codes'][lec_code])

driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')

if len(m_code) == 0: # No code specified ask for input
    code = input('Enter meet code: ')
else:
    code = creds['meet_codes'][lec_code]


# GMAIL LOGIN
driver.get(f'https://gmail.com/')
driver.find_element_by_xpath("//input[@type='email']").send_keys(creds['id'])
driver.find_element_by_xpath("//button[@jsname='LgbsSe']").click()

time.sleep(2)
driver.find_element_by_xpath("//input[@jsname='YPqjbf']").send_keys(creds['password'])
driver.find_element_by_xpath("//button[@jsname='LgbsSe']").click()


# MEET REDIRECT
time.sleep(4)
driver.get(f'https://meet.google.com/{code}')