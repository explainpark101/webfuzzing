"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from urllib.parse import parse_qs, quote_from_bytes, urlencode, urlparse, urljoin
from Search.payloads import fuzzer_payloads
from bs4 import BeautifulSoup, Comment
from Utils.utils import RandomString
from base64 import b64decode
from Crawler import sessions

__all__ = [
    'ReflectedXSS',
    'OpenRedirect',
    'SQLInjection',
    'CrossSiteRequestForgery',
    'NOSQLInjection',
    'OSCommandInjection',
    'ServerSideTemplateInjection',
    'LocalFileInclusion',
    'RemoteFileInclusion'
]

def init_session():
    return sessions()(Site=False)

class OpenRedirect:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

# class ReflectedXSS:
#     def __init__(self, current_url, html, headers, cookies, data, method, **info):
#         self.element_xss, self.attribute_xss, self.script_xss = fuzzer_payloads.xss()
#         self.current_url = current_url
#         self.sess = sessions().init_sess()
#         self.info = info
#         self.html = html
#         self.exploit(
#             headers = headers,
#             cookies = cookies,
#             data = data,
#             method = method,
#         )
 
#     def exploit(self, *, headers, cookies, data, method):
#         """
#         if urlparse(self.current_url).query:
#             쿼리가 있는 경우 체크
#             self.InputValueCheck(parse_qs(urlparse(self.current_url).query), 'qs')
#         if cookies:
#             self.InputValueCheck(cookies, 'cookies')
#         if haders:
#             self.InputValueCheck(headers, 'headers')
#         """
#         self.urinfo = urlparse(self.current_url)
#         if self.urinfo.query:
#             self.InputValueCheck(method, parse_qs(self.urinfo.query), 'params')
#         if data:
#             self.InputValueCheck(method, data, 'data')
#         if cookies:
#             self.InputValueCheck(method, cookies, 'cookies')
#         if headers:
#             self.InputValueCheck(method, headers, 'headers')

#     def InputValueCheck(self, method, _input, space):
#         """
#         먼저 해당 페이지에 출력이 되어 있는지 체크 한 다음 RandomString(5)를 이용하여 랜덤 값 체크
#         """
#         for key, value in _input.items():
#             soup = BeautifulSoup(self.html, 'html.parser')
#             if type(value) == list:
#                 value = value[0]
#             if soup.find_all(text=value) or (True in [value in j for i in soup.find_all() for j in i.attrs.values()]) or (soup.text.find(value) != -1):
#                 self.RequestRandomString(method, _input, key, space)

#     def RequestRandomString(self, method, _input, key, space):

#         randstr = RandomString(5)
#         temp = _input
#         temp[key] = randstr
#         if space == 'params':
#             r = self.sess.request(method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **self.info)
#         else:
#             r = self.sess.request(method, self.current_url, **{space:temp}, **self.info)
#         if randstr in r.text:
#             soup = BeautifulSoup(r.text, 'html.parser')
#             if soup.find_all(text=randstr) or(True in [randstr in j for i in soup.find_all() for j in i.attrs.values()]) or (soup.text.find(randstr) != -1):

#                 self.payloads_check(method,space, key,temp)

#     def payloads_check(self, method, space, key, _input = {''}):
#         for element in self.element_xss:
#             temp = _input
#             attrs_key_rand = RandomString(5)
#             attrs_value_rand = RandomString(5)
#             inner_text_rand = RandomString(5)
#             temp[key] = element.format(f" {attrs_key_rand}={attrs_value_rand}", inner_text_rand)
#             if space == 'params':
#                 r = self.sess.request(method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **self.info)
#             else:
#                 r = self.sess.request(method, self.current_url, **{space:temp}, **self.info)
#             soup = BeautifulSoup(r.text, 'html.parser')
#             if soup.find(attrs={attrs_key_rand.lower():attrs_value_rand}, text=inner_text_rand) or soup.find(attrs={attrs_key_rand.lower():attrs_value_rand}):
#                 print("\033[90m","="*50,"\033[0m")
#                 print(self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl())
#                 print(f'\033[31m[{urlparse(self.current_url).path}] : {space} attack vector discover\033[0m')
#                 print(f'\033[32m{_input}\033[0m')
#                 break
#         for attr in self.attribute_xss:
#             pass
#         for script in self.script_xss:
#             pass
#         # print("\033[90m","="*50,"\033[0m")
#         # print(f'\033[31m[{urlparse(self.current_url).path}] : {space} attack vector discover\033[0m')
#         # print(f'\033[32m{_input}\033[0m')


#         # vector : query string, cookies, headers
#         # print("\033[90m","="*50,"\033[0m")
#         # print(f'\033[31m[{urlparse(self.current_url).path}] : {vector} attack vector discover\033[0m')
#         # print(f'\033[32m{_input}\033[0m')

class ReflectedXSS:
    def __init__(self, current_url, html, headers, cookies, data, method, **info):
        self.element_xss, self.attribute_xss, self.script_xss = fuzzer_payloads.xss()
        self.urinfo = urlparse(self.current_url)
        self.current_url = current_url
        self.sess = sessions().init_sess()
        self.method = method
        self.info = info
        self.html = html

        if self.urinfo.fragment:
            self.search_text('fragment', '', '', self.urinfo.fragment)
        if self.urinfo.query:
            for key, value in self.urinfo.query.items():
                self.search_text('query', self.urinfo.query, key, value)
        if data:
            for key, value in data.items():
                self.search_text('data', data, key, value)
        if cookies:
            for key, value in cookies.items():
                self.search_text('cookies', cookies, key, value)
        if headers:
            for key, value in headers.items():
                self.search_text('headers', headers, key, value)

    def search_text(self, location, params, key, value):
        if (['fragment', 'query'] in location) and (value in self.html):
            self.random_string_search_text(location, params, key, value)
        else:
            self.random_string_search_text(location, params, key, value)

    def random_string_search_text(self):
        pass

    """def exploit(self, fragment, **input):
        if fragment:
            self.search_text('', 'fragment', fragment)
        for key, value in input:
            for _key, _value in value.items():
                self.search_text(key, _key, _value)


    def search_text(self, key, location, value):
        if value in self.html:
            self.random_string_search_text(key, location, value)

    def random_string_search_text(self, location, value):

        rand = RandomString(5)

        if ['fragment', 'query'] == location:
            if 'query':
                value[]
            r = self.sess.request(method = self.method, url = self.urinfo._replace(location=))
        else:
            value[location] = rand"""
            
    
    def html_injection_test_search_text(self):
        
        return True
        return False

    def xss_payloads_search_text(self):
        
        return True
        return False

class SQLInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class CrossSiteRequestForgery:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class NOSQLInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class OSCommandInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class ServerSideTemplateInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class LocalFileInclusion:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class RemoteFileInclusion:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL
