from selenium import  webdriver

b = webdriver.Firefix()
b.get('http://www.baidu.com')
b.title
b.current_url
b.maximize_window()