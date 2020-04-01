from bs4 import BeautifulSoup 
from crawler_rent.models import RentCrawler
from requests.packages import urllib3
from crawler_rent.config import URL_DICT, region_map
from urllib.parse import urlencode
from datetime import datetime
import logging
import re
import requests
import json
import time
import math
import random


urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Rent591Crawler(RentCrawler):
    def __init__(self, base_url):
        super().__init__(base_url)

    def _crawl(self, region):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # rent_list = []
        with requests.Session() as sess:
            headers['user-agent'] = random.choice(URL_DICT['rent591']['headers'])
            for post_id, region_name, nick_name, fulladdress, url in self._get_allurl_list(sess, region, headers):
                rent_out = self._get_rent_info(url, sess)
                identification, name = nick_name.split()[0], nick_name.split()[1]
                update_dict = {"_id": region_name.encode("cp950", "ignore").decode("cp950", "ignore") + '_' + str(post_id), "region": region_name.encode("cp950", "ignore").decode("cp950", "ignore"), "出租者": name.encode("cp950", "ignore").decode("cp950", "ignore"), "出租者身份": identification.encode("cp950", "ignore").decode("cp950", "ignore"), "地址": fulladdress.encode("cp950", "ignore").decode("cp950", "ignore")}
                rent_out.update(update_dict)
                key_order = ["_id", "region", "url", "出租者", "出租者身份", "聯絡電話", "租金", "型態", "現況", "性別要求", "地址", "update_time"]
                k = {k: rent_out[k] for k in key_order}
                yield k
                # rent_list.append(rent_out)
                # yield rent_out  # for upsert mongodb

    def _get_val(self, sess, region, headers):
        base_url = self.base_url + region_map[region]
        res = sess.get(base_url, headers=headers)
        res.encoding = 'utf-8'
        res.cookies['urlJumpIp'] = region_map[region]
    #     print(res.cookies.get_dict())
        soup = BeautifulSoup(res.text, "lxml")
    #     print(soup.select('head > meta'))
        try:
            totalRows = soup.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a.pageNext')[0]['data-total'] if soup.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a.pageNext') != [] else soup.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a:nth-child(16)')[0]['data-total']
        except Exception as e:
            print(e)
            totalRows = soup.find("a", {"class": "pageNum-form"})["data-total"] if soup.find("a", {"class": "pageNum-form"}) is not None else ""
        csrf_token = [i['content'] for i in soup.select('head > meta[name]') if i['name'] == "csrf-token"][0] if [i['content'] for i in soup.select('head > meta[name]') if i['name'] == "csrf-token"] != [] else ""

        return (totalRows, csrf_token)

    def _get_allurl_list(self, sess, region, headers):
        pattern = r"=$"
        val_list = []
        val = self._get_val(sess, region, headers)
        val_list.append(val)
        if val == ("", ""):
            val = val_list[-2]
            print(f"totalRows: {val[0]}, csrf_token: {val[1]}")
        # exc_resp = sess.get(self.base_url + region_map[region])
        # soup_exc = BeautifulSoup(exc_resp.text, 'html.parser')
        # if val[1] == []:
        #     val[1] = [i['content'] for i in soup_exc.select('head > meta[name]') if i['name'] == "csrf-token"][0]
        # if val[0] == "":
        #     val[0] = soup_exc.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a.pageNext')[0]['data-total']

        headers.update({'X-CSRF-TOKEN': val[1]})
        print(f"headers:{headers}")
        times = math.floor(int(val[0]) / 30) + 1 if int(val[0]) % 30 != 0 else math.floor(int(val[0]) / 30)

        for firstRow in range(times):
            searchurl = self._get_rent_list(sess, firstRow, region, headers)
            searchurl = searchurl + val[0] if re.search(pattern, searchurl) else searchurl   
            print(searchurl)
            try:    
                res_search = sess.get(searchurl, headers=headers)
                res_search.encoding = 'utf-8'
                data = json.loads(res_search.text)
        #         print(data['data']['data'][0]['post_id'])
                for i in data['data']['data']:
                    yield i['post_id'], i['region_name'], i['nick_name'], i['region_name'] + ' ' + i['fulladdress'], 'https://rent.591.com.tw/rent-detail-' + str(i['post_id']) + '.html'
                time.sleep(random.randint(1, 3))
                print(f"next page------------------------------------------------------------------") 
            except Exception as e:
                print(e)
                break
        #             yield rent_dict
    #         print(rent_list[0])      
        # print(f"the end------------------------------------------------------------------------")    

    def _get_rent_info(self, rent_url, sess):  # (self, rent_url, sess):
        if sess is None:
            r = requests.Session()
            rent_page = r.get(rent_url, headers=URL_DICT['rent591']['headers'], verify=False)
        else:
            rent_page = sess.get(rent_url, headers=sess.headers, verify=False)
        page = BeautifulSoup(rent_page.text, 'html.parser')
        url = rent_url
        phone = self._get_phone(page)
        money, form, situation = self._get_description(page)
        gender = self._get_condition(page)
    #     card_description = self._get_description(page)
    #     benefits = self._get_benefits(page)
    #     campaigns = self._get_campaigns(page)
        out = {
            "url": url,
            "region": "",
            "出租者": "", 
            "出租者身份": "", 
            "聯絡電話": phone,
            "租金": money,
            "型態": form,
            "現況": situation,
            "性別要求": gender,
            "update_time": datetime.now().isoformat()
        }
        return out

    def _get_phone(self, resp):
        try:
            phone = resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.userInfo > div:nth-child(2) > span.dialPhoneNum")[0]["data-value"] if resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.userInfo > div:nth-child(2) > span.dialPhoneNum") != [] else ""
        except Exception as e:
            print(e)
            phone = ""
        return phone

    def _get_description(self, resp):
        try:
            money = resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.detailInfo.clearfix > div.price.clearfix")[0].get_text().strip() if resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.detailInfo.clearfix > div.price.clearfix") != [] else "" 
            status = resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.detailInfo.clearfix > ul")[0].get_text() if resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.rightBox > div.detailInfo.clearfix > ul") != [] else ""
            form = ("".join(status[status.find("型態") + 2: status.find("現況")].split())).split(":")[1] if status != [] else ""
            situation = ("".join(status[status.find("現況") + 2: status.find("社區")].split())).split(":")[1] if status != [] else ""
        except Exception as e:
            print(e)
            form = ""
            situation = ""
        return money, form, situation

    def _get_condition(self, resp):
        try:
            condition = resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.leftBox > ul.clearfix.labelList.labelList-1")[0].get_text() if resp.select("#main > div.main_house_info.clearfix > div.detailBox.clearfix > div.leftBox > ul.clearfix.labelList.labelList-1") != [] else ""
    #         print(condition)
            gender = (condition[condition.find("性別要求") + 4:condition.find("性別要求") + 10]).split("：")[1] if condition != [] else ""
    #         print(gender)
            check_list = ['男女生皆可', '男生', '男性', '女生', '女性']
            for i in check_list:
                if gender.find(i) != -1:
                    gender = i
                    break
                else:
                    pass
            if gender not in check_list:
                gender = ""
        except Exception as e:
            print(e)
            gender = ""
        return gender

    # 獲取某縣市所有頁面url
    def _get_rent_list(self, sess, firstRow, region, headers):
        params = {
            'is_new_list': 1,
            'type': 1,
            'kind': 0,
            'searchtype': 1,
            'region': region,
            'firstRow': (firstRow * 30),
            'totalRows': self._get_val(sess, region, headers)[0]
        }
        base_url = URL_DICT['rent591']['rent_url']  # 'https://rent.591.com.tw/home/search/rsList?'
        url = base_url + urlencode(params)
        return url






