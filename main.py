import requests
import json
import os
from difflib import SequenceMatcher
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


class HotSearchScraper:
    def __init__(self, api_list, debug=0):
        self.api_list = api_list
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        self.debug = debug
        self.sender_email = os.environ.get('MAIL_SENDER')
        self.receiver_email = os.environ.get('MAIL_RECEIVER')
        self.password = os.environ.get('MAIL_PASSWORD')

    def fetch_data(self, urls):
        for url in urls:
            if self.debug:
                print(f"正在请求 URL: {url}")
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if self.debug:
                    print(f"请求 {url} 的状态码: {response.status_code}")
                    try:
                        print(f"请求 {url} 的返回数据: {response.json()}")
                    except json.JSONDecodeError:
                        print(f"请求 {url} 的返回数据不是有效的 JSON 格式: {response.text}")
                if response.status_code == 200:
                    return response.json()
                print(f"Request failed: {response.status_code} for {url}")
            except Exception as e:
                print(f"Request error: {str(e)} for {url}")
        return None

    def parse_baidu(self, data):
        if self.debug:
            print("正在解析百度数据...")
        try:
            return [item["title"] for item in data.get("data", [])]
        except (KeyError, TypeError):
            print("Failed to parse Baidu data.")
            return []

    def parse_weibo(self, data):
        if self.debug:
            print("正在解析微博数据...")
        try:
            return [item["title"] for item in data.get("data", [])]
        except (KeyError, TypeError):
            print("Failed to parse Weibo data.")
            return []

    def parse_zhihu(self, data):
        if self.debug:
            print("正在解析知乎数据...")
        try:
            return [item["title"] for item in data.get("data", [])]
        except (KeyError, TypeError):
            print("Failed to parse Zhihu data.")
            return []

    def parse_douyin(self, data):
        if self.debug:
            print("正在解析抖音数据...")
        try:
            return [item["title"] for item in data.get("data", [])]
        except (KeyError, TypeError):
            print("Failed to parse Douyin data.")
            return []

    def is_similar(self, s1, s2, threshold=0.8):
        return SequenceMatcher(None, s1, s2).ratio() >= threshold

    def remove_similar_terms(self, terms):
        if self.debug:
            print("正在去除相似词条...")
        unique_terms = []
        for term in terms:
            is_duplicate = False
            for unique_term in unique_terms:
                if self.is_similar(term, unique_term):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_terms.append(term)
        return unique_terms

    def filter_terms(self, terms):
        if self.debug:
            print("正在过滤词条，保留长度不少于 5 个字符的词条，并最多保留 100 条...")
        filtered_terms = [term for term in terms if len(term) >= 5]
        return filtered_terms[:100]

    def send_alert_email(self):
        if self.sender_email and self.receiver_email and self.password:
            msg = MIMEText('GitHub所有热搜 API 请求均失败，请检查网络或 API 状态。')
            msg['Subject'] = 'GitHub热搜 API 请求失败告警'
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email

            try:
                server = smtplib.SMTP_SSL('smtp.qq.com', 465)
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
                server.quit()
                print("告警邮件已发送。")
            except Exception as e:
                print(f"发送告警邮件时出错: {str(e)}")

    def process(self):
        if self.debug:
            print("开始处理数据...")
        all_terms = []
        all_failed = True
        for api in self.api_list:
            if self.debug:
                print(f"正在处理 {api['source']} 的数据...")
            if isinstance(api.get("url"), list):
                data = self.fetch_data(api["url"])
            elif isinstance(api.get("url"), str):
                data = self.fetch_data([api["url"]])
            else:
                print(f"Invalid URL configuration for {api['source']}")
                continue

            if data:
                all_failed = False

            if not data:
                continue

            parser = getattr(self, f"parse_{api['source']}", None)
            if not parser:
                print(f"No parser for {api['source']}")
                continue

            parsed_terms = parser(data)
            if parsed_terms:
                all_terms.extend(parsed_terms)

        if all_failed:
            self.send_alert_email()

        unique_terms = self.remove_similar_terms(all_terms)
        final_terms = self.filter_terms(unique_terms)
        if self.debug:
            print("数据处理完成。")
        return final_terms


if __name__ == "__main__":
    API_CONFIG = [
        {
            "source": "baidu",
            "url": [
                "https://api-hot.imsyy.top/baidu?cache=true",
                "https://uapis.cn/api/hotlist?type=baidu",
                "https://api.gmya.net/Api/BaiduHot"
            ],
            "parser": "parse_baidu"
        },
        {
            "source": "weibo",
            "url": [
                "https://uapis.cn/api/hotlist?type=weibo",
                "https://api-hot.imsyy.top/weibo?cache=true",
                "https://api.gmya.net/Api/WeiBoHot"
            ],
            "parser": "parse_weibo"
        },
        {
            "source": "zhihu",
            "url": [
                "https://api.gmya.net/Api/ZhiHuHot",
                "https://api-hot.imsyy.top/zhihu?cache=true",
                "https://uapis.cn/api/hotlist?type=zhihu"
            ],
            "parser": "parse_zhihu"
        },
        {
            "source": "douyin",
            "url": [
                "https://api-hot.imsyy.top/douyin?cache=true",
                "https://uapis.cn/api/hotlist?type=douyin",
                "https://api.gmya.net/Api/DouYinHot"
            ],
            "parser": "parse_douyin"
        }
    ]
    debug = 0  # 生产环境建议关闭调试模式
    # 只传入必要的参数
    scraper = HotSearchScraper(API_CONFIG, debug)
    hot_terms = scraper.process()

    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)
    filename = "hotkeys.json"
        # 获取当前时间
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建包含更新时间和热搜词条的字典
    data = {
        "update_time": update_time,
        "titles": hot_terms
    }
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(hot_terms)} unique hot terms to {filename}")
    
