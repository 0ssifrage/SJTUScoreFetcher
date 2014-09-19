import cookielib
import re
import urllib
import urllib2


class LoginError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ScoreFetcher(object):
    def __init__(self, s_id, s_pwd):
        self.__s_id = s_id
        self.__s_pwd = s_pwd

        self.__re_vs = re.compile('id="__VIEWSTATE" value="(.*?)"')
        self.__re_ev = re.compile('id="__EVENTVALIDATION" value="(.*?)"')
        self.__re_btn1 = re.compile('name="Button1" value="(.*?)"')
        self.__re_btns = re.compile('name="btnSearch" value="(.*?)"')

        url_base = 'http://electsys.sjtu.edu.cn/edu/'
        self.__url_index = url_base + 'index.aspx'
        self.__url_score = url_base + 'StudentScore/B_StudentScoreQuery.aspx'

    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        content = urllib2.urlopen(self.__url_index).read()
        vs = self.__re_vs.search(content).group(1)
        ev = self.__re_ev.search(content).group(1)
        btn = self.__re_btn1.search(content).group(1)

        post_data = urllib.urlencode({
            '__VIEWSTATE': vs,
            '__EVENTVALIDATION': ev,
            'txtUserName': self.__s_id,
            'txtPwd': self.__s_pwd,
            'rbtnLst': '1',
            'Button1': btn
        })
        req = urllib2.Request(self.__url_index, post_data)
        try:
            res = urllib2.urlopen(req).read()
        except urllib2.URLError, e:
            if e.code == 404:
                raise LoginError(
                    "Login too frequently. Please try again after 30s.")
        if "messagePage" in res:
            raise LoginError("Incorrect username or password.")

    def get_scores(self, xn="2013-2014", xq="2"):
        content = urllib2.urlopen(self.__url_score).read()
        vs = self.__re_vs.search(content).group(1)
        ev = self.__re_ev.search(content).group(1)
        btn_s = self.__re_btns.search(content).group(1)

        post_data = urllib.urlencode({
            '__VIEWSTATE': vs,
            '__EVENTVALIDATION': ev,
            'ddlXN': xn,
            'ddlXQ': xq,
            'txtKCDM': '',
            'btnSearch': btn_s
        })
        req = urllib2.Request(self.__url_score, post_data)
        res_html = urllib2.urlopen(req).read()
        re_score = re.compile('"180">(.*?) .*?>(\d+\.\d+)<.*?>(\d+\.\d+)<')
        scores = re_score.findall(res_html)

        return scores
