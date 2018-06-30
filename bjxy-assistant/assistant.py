from PIL import Image
import pytesseract


def recon_captcha():
    im = Image.open('captcha.jpg')
    gray = im.convert('L')
    # gray.show()

    threshold = 150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    out = gray.point(table, '1')
    # out.show()
    out.save("captcha_threshold.jpg")

    th = Image.open("captcha_threshold.jpg")
    return pytesseract.image_to_string(th)


def get_captcha(session, captcha_url):
    r = session.get(captcha_url)
    with open('captcha.jpg', "wb") as f:
        f.write(r.content)
        f.close()

    im = Image.open('captcha.jpg')
    im.show()
    im.close()
    captcha = input("captcha: ")
    return captcha


def login(session, headers, username, password, view_state, view_state_generator, web_site_url):
    post_data = {
        "__VIEWSTATE": view_state,
        "__VIEWSTATEGENERATOR": view_state_generator,
        "TextBox1": username,
        "TextBox2": password,
        "TxtYZM": get_captcha(session, web_site_url + "/yzm.aspx"),
        "js": "RadioButton3",
        "Button1": "登陆"
    }
    session.post(web_site_url + "/default.aspx", data=post_data, headers=headers)


def compute_weight_aver(soup):
    course_type = ["必修课", "公共基础", "公共基础课", "公共课", " 实习实践", "实习实践课",
                   "学年论文", "专业基础", "专业基础课", "专业课"]
    table = soup.select("#GridView1")[0]
    tr_list = table.select("tr[class='GridViewRowStyle'],tr[class='GridViewAlternatingRowStyle']")

    total_score = 0
    total_credit = 0
    for each_tr in tr_list:
        td_list = each_tr.select("td")
        if td_list[3].text in course_type and '体育' not in td_list[2].text:
            try:
                total_score += int(td_list[4].text) * int(td_list[7].text)
                total_credit += int(td_list[7].text)
            except ValueError:
                print(td_list[2].text)

    assert total_credit != 0
    return total_score / total_credit
