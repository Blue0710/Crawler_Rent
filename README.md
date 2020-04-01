# Rent591 Crawlers

## Run

```bash
python -m bin.main --help
# Loading .env environment variables...
# $ Usage: main.py [OPTIONS]

#Crawling Specify region

#Options:
#  -r, --region [台北市|基隆市|新北市|新竹市|新竹縣|桃園市|苗栗縣|台中市|彰化縣|南投縣|嘉義市|嘉義縣|
#雲林縣|台南市|高雄市|屏東縣|宜蘭縣|台東縣|花蓮縣|澎湖縣|金門縣|連江縣|all]
#                          Specify region (e.g, `-r '宜蘭縣'` or ˋ-r '台北市'
#                                  -r '新北市'ˋ)  [required]
 # --help                          Show this message and exit.


# run all region 
$ python -m bin.main -r 'all' 

# run specify region
$ python -m bin.main -r '台北市'

# run multiple region
$ python -m bin.main -r '台北市' -r '新北市'
```

## Data Sources

**rent591**
- https://rent.591.com.tw/?kind=0&regionid=


## Data Schema

```json
{
	"_id":"台北市_9029077",
	"region":"台北市",
	"url":"https://rent.591.com.tw/rent-detail-9029077.html",
	"出租者":"鐘先生",
	"出租者身份":"屋主",
	"聯絡電話":"0927-340-006",
	"租金":"19,999 元/月",
	"型態":"電梯大樓",
	"現況":"整層住家",
	"性別要求":"男女生皆可",
	"地址":"台北市 林森南路CKSMRT30sec中正紀念堂30秒",
	"update_time":"2020-03-29T15:37:35.338127",
	"first_seen_date":"2020-03-29T14:12:59.881864"
}
```

## Getting started

Run with environment variable settings in dotenv file as below:

**.env:**

```
# .env
MONGODB_HOST=******
MONGODB_PORT=******
MONGODB_DB=********
MONGODB_USER=******
MONGODB_PWD=*******

...
```


