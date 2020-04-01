from fake_useragent import UserAgent
ua = UserAgent()
user_agent_list = list()
for i in range(50):
    user_agent_list.append(ua.random)


DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

URL_DICT = {
    'rent591': {
        'region_url': 'https://rent.591.com.tw/?kind=0&regionid=',
        'rent_url': 'https://rent.591.com.tw/home/search/rsList?',
        # 'card_url': 'https://www.taishinbank.com.tw/TSB/personal/credit/intro/overview/index.html?type=type',
        'headers': user_agent_list,
    }
}

region_map = {
    '台北市': '1',
    '基隆市': '2',
    '新北市': '3',
    '新竹市': '4',
    '新竹縣': '5',
    '桃園市': '6',
    '苗栗縣': '7',
    '台中市': '8',
    '彰化縣': '10',
    '南投縣': '11',
    '嘉義市': '12',
    '嘉義縣': '13',
    '雲林縣': '14',
    '台南市': '15',
    '高雄市': '17',
    '屏東縣': '19',
    '宜蘭縣': '21',
    '台東縣': '22',
    '花蓮縣': '23',
    '澎湖縣': '24',
    '金門縣': '25',
    '連江縣': '26',
}

