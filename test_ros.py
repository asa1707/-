from array import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from time import sleep, time
import os
import sys

from random import randrange,randint

#import certifi
import ssl
import base64
import time


##################################################
# настройки

txt_proxy = '';


url_login = 'https://b2c.passport.rt.ru';

wrong_phone = '75559995533'
wrong_login = 'JabbaHutt'
wrong_email = 'JabbaHutt@mail.com'
wrong_password = '123321Qq'



##################################################

profile = webdriver.FirefoxProfile() 

if txt_proxy != '':
	profile.set_preference("network.proxy.type", 1)
	profile.set_preference("network.proxy.socks", txt_proxy[0] )
	profile.set_preference("network.proxy.socks_port", int(txt_proxy[1]) )
	profile.set_preference("network.proxy.socks_version", 5)
	profile.update_preferences()


######################################
# решение капчи, не знаю считать ли это за тест но как минимум надеюсь обратите внимание т.к это стоило многих усилий и по итогу число тестов не достаточное
def solve_cap():
	
	api_key = '927a533591c773afecd77dfbcebcf6c4'

	#a = driver.find_element_by_css_selector('.rt-captcha__image').click();
	#b = driver.find_element_by_css_selector('input.CheckboxCaptcha-Button').send_keys(Keys.RETURN)
	#print(a)

	#sleep(4)

	cimg = driver.find_element_by_css_selector('.rt-captcha__image').get_attribute('src');

	print('img: ' + cimg)

	sleep(1)

	request = Request(cimg);
	buf = urlopen(request).read()

	data = urlencode({'method':'base64', 'body': base64.b64encode(buf), 'key': api_key}).encode()
	request = Request('http://rucaptcha.com/in.php?key='+api_key, data);
	buf = urlopen(request).read().decode();
	print(buf);
	cid = buf.split('|')
	print('requested')

	for i in range(50):
		sleep(1)
		request = Request('http://rucaptcha.com/res.php?key='+api_key+'&action=get&id='+cid[1]);
		buf = urlopen(request).read().decode();
		print('res: '+buf)
		if (buf != 'CAPCHA_NOT_READY') :
			break


	driver.find_element_by_css_selector('#captcha').send_keys(buf.split('|')[1])


####################################################
# проверка всех форм логина с выводом сообщения - "не верные логин + пароль"	

####################################################
# проверка на некорректный номер телефона
# логин по телефону - вкладка №1
print('start - запускаем браузер')

driver = webdriver.Firefox(firefox_profile=profile)

##########################################################################################################################################################

def get_driver():

    global driver

    driver.get(url_login)

    wait = WebDriverWait(driver, 30)
    assert wait.until(
        EC.presence_of_element_located((By.XPATH, '//h1[@class="card-container__title"]'))).text == 'Авторизация'
    return driver, wait

# переход в vk
def test_vk():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()
    time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать

    assert driver.current_url.__contains__('oauth.vk.com')



#  Переход в однокласники
def test_ok():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()
    time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать

    assert driver.current_url.__contains__('connect.ok.ru')


#  Переход в Mail.ru
def test_mail():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()
    time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать

    assert driver.current_url.__contains__('connect.mail.ru')


#  Переход в аккаунт Google
def test_google():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()
    time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать

    assert driver.current_url.__contains__('accounts.google.com')


#  Переходв Yandex
def test_yandex():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()
    time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать

    assert driver.current_url.__contains__('oauth.yandex.ru')
    time.sleep(2)

def test_recovery(): #  Проверка открытия страницы востановления пароля
    driver, wait = get_driver()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, 'forgot_password'))).click()
    time.sleep(2)
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Восстановление пароля'
    time.sleep(2)

def test_register(): #  Проверка открытия страницы регистрации
    driver, wait = get_driver()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    time.sleep(2)
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'
    time.sleep(2)


#def test_registration_number(): #  Проверка регистрации по номеру телефона - страница Регистрации
   # driver, wait = get_driver()
    #actionChain #= ActionChains(driver)

    #wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
   # assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'
   # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
   # actionChain.send_keys('Sergo123').perform()
  #  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
   # actionChain.send_keys('Sergo123').perform()
   # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    #actionChain.send_keys('+79650694568').perform()
    #wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
  #  actionChain.send_keys('Абалакин').perform()
  #  wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
  #  actionChain.send_keys('Сергей').perform()
   # time.sleep(2) # Для наглядности - в реальности тестирования закоментировать
    #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div > div > div:nth-of-type(2) > svg'))).click()
#    time.sleep(2) # Для наглядности - в реальности тестирования закоментировать
 #   wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div:nth-of-type(2) > div > div:nth-of-type(2) > svg > path'))).click()
  #  time.sleep(5) # Для наглядности - в реальности тестирования закоментировать
  #  driver.find_element(By.NAME, 'register').click()
  #  time.sleep(3) # Для наглядности - в реальности тестирования закоментировать

   # confirmPage = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Подтверждение телефона')]"))).text
   # assert confirmPage == 'Подтверждение телефона'


#def test_form_change():  #  Проверка изменения подсказки текста плейсхолдера в поле "Логин" при изменении


    # способа авторизации формы авторизация
 #   driver, wait = get_driver()
 #   actionChain = ActionChains(driver)

 #   wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
 #   assert wait.until(EC.presence_of_element_located(
 #       (By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'
 #   tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))

 #   assert wait.until(EC.title_is('Ростелеком ID'))
 #   assert len(tabButtons) == 4

 #   for i in range(len(tabButtons)):
 #       actionChain.move_to_element(tabButtons[i]).click().perform()
 #       placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
 #       time.sleep(2)  # Для наглядности - в реальности тестирования закоментировать
 #       assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tab--active'))).text == driver.find_element(
 #           By.ID, consts.tabButtonsId[i]).text
 #       assert placeholderInput == consts.placeholderInputsValue[i]




def test_back_to_login(): #  Проверка функциональности кнопки "Вернуться назад", на странице Восстановление пароля
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'
    time.sleep(1)

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='reset-back']"))).click()
    time.sleep(2)


#сюда вставлять тесты

test_back_to_login()
#test_form_change()
#test_registration_number()
test_register()
test_recovery()
test_yandex()
test_google()
test_mail()
test_vk()
test_ok()


driver.get(url_login)

driver.implicitly_wait(10) # неявное ожидание пока появится форма логина 10 сек

# кликаем на вкладку телефон
el = driver.find_element_by_id('t-btn-tab-phone')
el.click();

el = driver.find_element_by_id('username')

# пытаемся ввести некореектный номер
el.send_keys('5555')

el = driver.find_element_by_id('password')
el.send_keys(wrong_password)


el2 = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container__meta--error')
if (len(el2) > 0) and (el2[0].get_attribute('innerHTML') == 'Неверный формат телефона'):
	print("Тест на некорректный номер пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный номер НЕ пройден. ОШИБКА! " );
print('####################################################')


sleep(3)



#################################################################################################################################




# логин по телефону - вкладка №1

# кликаем на вкладку телефон
el = driver.find_element_by_id('t-btn-tab-phone')
el.click();

print("Вводим не верный номер телефона и пароль")
el = driver.find_element_by_id('username')

# пытаемся ввести некореектный номер
el.send_keys(wrong_phone)

# проверяем не появилась ли капча
el2 = driver.find_elements_by_css_selector('.rt-captcha')
if (len(el2) > 0):
	#input("Найдена капча... введите в окне капчу и нажмите здесь - ENTER");
	print("Решаем капчу автоматически...");
	solve_cap()



el = driver.find_element_by_id('password')
el.send_keys(wrong_password)



driver.find_element_by_css_selector('#kc-login').click();


el2 = driver.find_elements(By.ID, 'form-error-message')
if (len(el2) > 0):
	print("Тест на некорректный номер + пароль пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный номер + пароль НЕ пройден. ОШИБКА! " );
print('####################################################')



####################################################
# логин по телефону - вкладка №2

# кликаем на вкладку телефон
el = driver.find_element_by_id('t-btn-tab-mail')
el.click();

print("Вводим не верный email и пароль")
el = driver.find_element_by_id('username')

# пытаемся ввести некореектный номер
el.send_keys(wrong_email)

# проверяем не появилась ли капча
el2 = driver.find_elements_by_css_selector('.rt-captcha')
if (len(el2) > 0):
	#input("Найдена капча... введите в окне капчу и нажмите здесь - ENTER");
	print("Решаем капчу автоматически...");
	solve_cap()



el = driver.find_element_by_id('password')
el.send_keys(wrong_password)



driver.find_element_by_css_selector('#kc-login').click();


el2 = driver.find_elements(By.ID, 'form-error-message')
if (len(el2) > 0):
	print("Тест на некорректный email + пароль пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный email + пароль НЕ пройден. ОШИБКА! " );
print('####################################################')




####################################################
# логин по логину - вкладка №3

# кликаем на вкладку телефон
el = driver.find_element_by_id('t-btn-tab-login')
el.click();

print("Вводим не верный login и пароль")
el = driver.find_element_by_id('username')

# пытаемся ввести некореектный номер
el.send_keys(wrong_login)

# проверяем не появилась ли капча
el2 = driver.find_elements_by_css_selector('.rt-captcha')
if (len(el2) > 0):
	#input("Найдена капча... введите в окне капчу и нажмите здесь - ENTER");
	print("Решаем капчу автоматически...");
	solve_cap()



el = driver.find_element_by_id('password')
el.send_keys(wrong_password)



driver.find_element_by_css_selector('#kc-login').click();


el2 = driver.find_elements(By.ID, 'form-error-message')
if (len(el2) > 0):
	print("Тест на некорректный login + пароль пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный login + пароль НЕ пройден. ОШИБКА! " );
print('####################################################')


sleep(3)




####################################################
# логин по лицевому счету - вкладка №4

# кликаем на вкладку телефон
el = driver.find_element_by_id('t-btn-tab-ls')
el.click();

print("Вводим не верный лицевой счет и пароль")
el = driver.find_element_by_id('username')

# пытаемся ввести некореектный номер
el.send_keys(wrong_phone)

# проверяем не появилась ли капча
el2 = driver.find_elements_by_css_selector('.rt-captcha')
if (len(el2) > 0):
	#input("Найдена капча... введите в окне капчу и нажмите здесь - ENTER");
	print("Решаем капчу автоматически...");
	solve_cap()



el = driver.find_element_by_id('password')
el.send_keys(wrong_password)



driver.find_element_by_css_selector('#kc-login').click();


el2 = driver.find_elements(By.ID, 'form-error-message')
if (len(el2) > 0):
	print("Тест на некорректный лицевой счет + пароль пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный лицевой счет + пароль НЕ пройден. ОШИБКА! " );
print('####################################################')






####################################################
# Регистрация

# кликаем на вкладку телефон
print('идем на регистрацию')
el = driver.find_element_by_id('kc-register')
el.click();

print("Регистрация - Вводим не верный телефон и пароль")
el = driver.find_element_by_id('address')

# пытаемся ввести некореектный номер
el.send_keys('75556')






el = driver.find_element_by_id('password')
el.send_keys(wrong_password)

sleep(2)

el2 = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container__meta--error')
if (len(el2) > 0):
	print("Тест на некорректный номер пройден! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на некорректный номер НЕ пройден. ОШИБКА! " );
print('####################################################')

sleep(1)

el = driver.find_element_by_id('address')

# пытаемся ввести некореектный номер
el.send_keys(Keys.CONTROL + "a")
el.send_keys(Keys.DELETE)
el.send_keys('v.zoomx@ya.ru')



el = driver.find_element_by_id('password-confirm')
el.send_keys(wrong_password)



# проверяем не появилась ли капча
el2 = driver.find_elements_by_css_selector('.rt-captcha')
if (len(el2) > 0):
	#input("Найдена капча... введите в окне капчу и нажмите здесь - ENTER");
	print("Решаем капчу автоматически...");
	solve_cap()



el = driver.find_element_by_css_selector('input[name=firstName]')
el.send_keys('Петр')
el = driver.find_element_by_css_selector('input[name=lastName]')
el.send_keys('Иванов')


driver.find_element_by_css_selector('button[name=register]').click();


el2 = driver.find_elements(By.CLASS_NAME, 'card-modal__title')
if (len(el2) > 0):
	print("Тест на регистрацию существующего аккаунта - ПРОЙДЕН! - ", el2[0].get_attribute('innerHTML') );
else:
	print("Тест на регистрацию существующего аккаунта - НЕ пройден. ОШИБКА! " );
print('####################################################')

sys.exit();

sleep(3)


