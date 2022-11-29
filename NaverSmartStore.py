from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip


class NaverSmartStore:
    __driver = None
    __url = None
    __fileName = None

    def setData(self, url, fileName):
        self.__url = url
        self.__fileName = fileName

    def __init__(self, url, fileName):
        self.setData(url, fileName)

    # 실행
    def Play(self):
        self.start()
        self.login()
        self.action()

    # 전개
    def start(self):
        chrome_ver, option = self.__getChrome()
        self.__getDriver(chrome_ver, option)
        self.__getUrl(self.__url)

    # 로그인
    def login(self):
        info = self.__userImport(self.__fileName)
        self.__userInput(info['ID'], info['PW'])

    # 동작
    def action(self):
        self.__modalClose()
        # 신규주문 클릭
        self.__driver.find_element_by_css_selector('a[ng-bind="::vm.saleStats.newOrderCases"]').click()
        # iframe 전환 및 세부 사항 적용, 엑셀 다운
        self.__driver.switch_to.frame('__naverpay')
        self.__orderConfirm
        # self.__Accept()
        # self.__downloadExcel()

    # 크롬 디버거 창으로 새 창 열기
    def __getChrome(self):
        subprocess.Popen(
            r'C:/Program Files (x86)/Google\Chrome/Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/chrometemp"')  # 디버거 크롬 구동

        option = Options()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        option.add_experimental_option("detach", True) #Run Python File in Terminal로 실행 시 추가할 필요 없음

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        return chrome_ver, option

    def __getDriver(self, chrome_ver, option):
        try:
            self.__driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        except:
            chromedriver_autoinstaller.install(True)
            self.__driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        self.__driver.implicitly_wait(10)

    def __getUrl(self, url):
        self.__driver.get(url)

    # 사용자 정보 가져오기
    def __userImport(self, fileName):
        info = {}
        with open(f"C:/Users/juno/Python/프로젝트(닥터트루)/Master_key/{fileName}.txt") as f:
            for line in f:
                key, value = line.strip().split(' : ')
                info[key] = value
        return info

    # 사용자 정보 클립보드 복사후 로그인
    def __userInput(self, ID, PW):
        # 사용자 클립보드 생성
        def clipInput(self, user_xpath, user_input):
            temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

            pyperclip.copy(user_input)
            self.__driver.find_element_by_xpath(user_xpath).click()
            ActionChains(self.__driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴

        login = {
            "id": f"{ID}",
            "pw": f"{PW}"
        }

        clipInput(self, '//*[@id="id"]', login.get("id"))
        clipInput(self, '//*[@id="pw"]', login.get("pw"))
        self.__driver.find_element_by_xpath('//*[@id="log.login"]').click()
        if self.__driver.current_url == "https://nid.naver.com/login/ext/deviceConfirm.nhn?svctype=1&locale=ko_KR&url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523&id=icde0523&key=u44hJOGF9TppvSfWN4NQexFavF5gEBvELhLuUlKK2kSj51BKuD05o6hpn-jdMPzYCUUnEGjoBXMA75cOoxEhtePRrYgs14LlLg0b-HARm1dJiffStphR_5uzBAqLOH6j3e7Z_s6wWoTFFaTahF-ogxJY9Pl5zQX9bf9WYu1O009sbP1475cgxBuSU3IDBnghT2x9Wvo2FaUYOfG639BFPOmWBmp-Ogefg53-6gdif2tgzmyHL4Kp98C3KA2gCL-XkS8G4gwBZmNBxCHy_tpyg3FRUqvWKSPFFvl5ralXWb4sDLGI8KXzq9cvT5eLJ7hcVY94alll2RYx8iEGxUrwsKK-304OMQ5Fyyg0bSHBaXZl7Lwmld0Q4sdIKkCGAytiE2rCLlyaT1PNFsmSxT8KHUJGIcRtvQ25Rxvts-gfbGIYyRAX9vClii7MwdQ0BiXE":
            self.__driver.find_element_by_id('new.dontsave').click()

    # Modal창 닫기
    def __modalClose(self):
        try:
            self.__driver.find_element_by_xpath(
                '//*[@id="seller-content"]/div/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button/span').click()
        except:
            pass

    # 신규주문~발주확인
    def __orderConfirm(self):
        # 신규주문 탭
        try:
            self.__driver.find_element_by_xpath(
                '//*[@id="__app_root__"]/div/div[2]/div[2]/div/div[2]/ul/li[3]/div/a[1]').click()
        except:
            pass
        # 체크박스 전체선택
        self.__driver.find_element_by_xpath(
            '//*[@id="__app_root__"]/div/div[2]/div[4]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr/th[1]/div').click()
        # 발주 확인
        self.__driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[4]/div[2]/button[1]')

    # 검색
    # driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[3]/div[2]/button').click()

    # 발주확인~엑셀다운
    def __downloadExcel(self):
        # 발주확인 탭
        try:
            self.__driver.find_element_by_xpath(
                '//*[@id="__app_root__"]/div/div[2]/div[2]/div/div[2]/ul/li[4]/div/a[1]').click()
        except:
            pass
        # 체크박스 전체선택
        self.__driver.find_element_by_xpath(
            '//*[@id="__app_root__"]/div/div[2]/div[4]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr/th[1]/div').click()
        # 엑셀 다운
        self.__driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[4]/div[1]/div/button[2]').click()

    # 확인 메시지
    def __accept(self):
        try:
            self.__driver.switch_to.alert.accept()
        except:
            pass

if __name__=='__main__':
    url = 'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523'
    fileName = 'naver_smart_store'
    naver = NaverSmartStore(url, fileName)
    naver.start()
    #naver.login()
    #naver.action()
    