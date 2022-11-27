from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller
# import subprocess
# import shutil

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import schedule

from webdriver_manager.chrome import ChromeDriverManager


def getDriver(url):
    # def onDebugger(options, debugger):
    #     if debugger == True:
    #         try:
    #             shutil.rmtree(r"c:/chrometemp")  # 쿠키 / 캐쉬파일 삭제
    #         except FileNotFoundError:
    #             pass
    #         subprocess.Popen(
    #             r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe --remote-debugging-port=9222 --user-data-dir="C:/chrometemp"')  # 디버거 크롬 구동
    #         options.add_experimental_option(
    #             "debuggerAddress", "127.0.0.1:9222")
    #     else:
    #         options.add_argument('--headless')
    #     return options

    # options = Options()
    # options = onDebugger(options, True)

    # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # service = Service(executable_path=ChromeDriverManager().install())
    # try:
    #     driver = webdriver.Chrome(service=service, options=options)
    # except:
    #     chromedriver_autoinstaller.install(True)
    #     driver = webdriver.Chrome(service=service, options=options)
    # driver.implicitly_wait(10)
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    return driver


def getData(driver):
    # text = driver.find_elements(
    #     by=By.XPATH, value='//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div/div[1]/div[1]/a/span[2]')
    # print(text[0].text)
    print("----------------------------------------")
    for i in range(1, 3):
        for j in range(1, 6):
            num = driver.find_elements(
                by=By.XPATH, value=f'//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div/div[{i}]/div[{j}]/a/span[1]')[0].text
            text = driver.find_elements(
                by=By.XPATH, value=f'//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div/div[{i}]/div[{j}]/a/span[2]')[0].text
            print(num, " : ", text)


if __name__ == '__main__':
    url = 'https://www.signal.bz/'
    driver = getDriver(url)
    getData(driver)
    schedule.every(5).seconds.do(getData, driver)
    while True:
        schedule.run_pending()
