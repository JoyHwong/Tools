import requests
from bs4 import BeautifulSoup
import assistant

session = requests.session()
r = session.get("http://sql.bjxy.cn")
web_site_url = r.url[0:-13]
soup = BeautifulSoup(r.content, "html.parser")
view_state = soup.select("input[name='__VIEWSTATE']")[0]['value']
view_state_generator = soup.select("input[name='__VIEWSTATEGENERATOR']")[0]['value']
username = input("username: ")
password = input("password: ")


agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) " \
        "Chrome/67.0.3396.99 Safari/537.36"
headers = {
    'User-Agent': agent,
    "host": "sql.bjxy.cn",
    "Referer": web_site_url + "/Default.aspx"
}

assistant.login(session, headers, username, password, view_state, view_state_generator, web_site_url)

score_page_source = session.get(web_site_url + "/student/chengji.aspx")
soup = BeautifulSoup(score_page_source.content, "html.parser")
if len(soup.select("iframe[name='I1']")) != 0:
    print("密码或验证码错误或半小时内登陆次数超过上限")
else:
    print(assistant.compute_weight_aver(soup))
