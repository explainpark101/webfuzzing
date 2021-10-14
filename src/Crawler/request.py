from selenium.webdriver import Chrome, ChromeOptions
from . import __globals__ as var
from urllib.parse import urljoin
import requests
import os

class sessions:
    def __init__(self, url, **args) -> None:
        self.url = url
        self.arguments = args
        self.sess_check = False
        self.CONFIG = var.SELENIUM_CONFIG
        self.path = os.getcwd() + (var.NT_PATH if os.name == "nt" else var.POSIX_PATH)
        self.driver = False

        self.sess = requests.Session()
        
    def __call__(self, url, **args : dict) -> dict:
        self.url = url
        self.arguments = args

    def driver_set(self, url) -> str:
        self.url = url

        return self.driver_get()

    def sess_rtn(self, response) -> dict:
        return {
            'status': response.status_code,
            'history':response.history,
            'headers':response.headers,
            'cookies':response.cookies,
            'body':response.content.decode("utf-8", "replace"),
            'url':response.url,
            'conn':response.ok,
            'request':response.request
        }

    def sess_set_get(self, url, **arguments) -> dict:
        self.url = url
        self.arguments = arguments

        return self.sess_get()

    def sess_set_post(self, url, **arguments) -> dict:
        self.url = url
        self.arguments = arguments
        
        return self.sess_get()

    def sess_get(self) -> dict:

        res = self.sess.get(self.url, **self.arguments)
        return self.sess_rtn(res)


    def sess_post(self) -> dict:

        res = self.sess.post(self.url, **self.arguments)

        return self.sess_rtn(res)

    def driver_get(self) -> str:
        try:

            if self.driver:
                self.drive.get(self.url)
                return {
                    'status': 200,
                    'url':self.drive.current_url,
                    'body':self.drive.page_source,
                }

            else:
                return self.webdriver()

        except:

            return {
                'status': 200,
                'url':self.drive.current_url,
                'body':'',
            }

    def WebDriverChromeWS(self) -> bool:
        try:
            self.options = ChromeOptions()

            for _ in self.CONFIG:
                self.options.add_argument(_)
            self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            self.drive = Chrome(self.path, options=self.options)
            self.drive.implicitly_wait(5)
            self.drive.set_page_load_timeout(5)
            self.drive.get(urljoin(self.url,"/"))
            self.driver = True

            return True
        except:
            return False

    def webdriver(self) -> str:
        self.WebDriverChromeWS()
        
        return {
            'status': 200,
            'url':self.drive.current_url,
            'body':self.drive.page_source,
        }

    def DriveAlertCheck(self, url) -> dict:
        if not self.driver:
            self.WebDriverChromeWS()
        self.drive.get(url)

        try:
            Alert = self.drive.switch_to.alert
            return {
                'alert':Alert.text
            }
        except:
            return {
                'alert':None
            }

    def __del__(self) -> None:
        self.sess.close()
        if self.driver: self.drive.quit()