import json
import re
from typing import Iterable

import requests
import scrapy
from Tools.scripts.generate_opcode_h import header
from scrapy import Request


class BilivideoSpider(scrapy.Spider):
    name = "bilivideo"
    allowed_domains = ["www.bilibili.com"]
    # start_urls = ["https://www.bilibili.com/video"]
    base_url = f"https://www.bilibili.com/video/BV1u84y1X7s5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Referer":base_url,
        "cookie": "buvid3=728DF2A2-7F59-F5D3-3E33-529CFAECEF3C91689infoc; b_nut=1727425491; _uuid=F126631E-1087D-10D87-EB74-294CA6E586CA91995infoc; buvid4=7BEE92FF-6B7A-48AA-506C-15BE3F67C22992679-024092708-TMpdmdQTOL0eld9TU91%2F9g%3D%3D; buvid_fp=36bb8831f81dd2bdcb4c384bc477126a; rpdid=|(J|YJkm)RYY0J'u~k~RklRmR; header_theme_version=CLOSE; enable_web_push=DISABLE; home_feed_column=5; DedeUserID=18516237; DedeUserID__ckMd5=36d9a216a28eecbf; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzU1NDY4MzcsImlhdCI6MTczNTI4NzU3NywicGx0IjotMX0.jEoVt53D59isS7cc897s7hKsWnlyg54f56nnZONWAt8; bili_ticket_expires=1735546777; SESSDATA=2aecc8be%2C1750839657%2Cf1fa1%2Ac1CjAI1qZw_5a5F_aQUcxWOdJ54WTJbj1BlVvcfUQRmZVJXopt3NgKx8b1g3F6yq4CNF4SVmFUVlkwVWxWNmFMSXZ5eHpZRlNaZ1p6ajVjMlpHcHMxM3dtOGJXRHdxUGJDWUMwcE90VDVBRC0yVjlmd2FDRTEzNUNZSnNiMC1oUHZYcDFCRjdiSk9BIIEC; bili_jct=09b072b4f6a88c42b4939e6ad38e1ce1; sid=82twx2c0; bp_t_offset_18516237=1015543810253389824; b_lsid=2610D10424_1941513281C; bsource=search_bing; browser_resolution=1492-848; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; CURRENT_FNVAL=4048"
    }
    def start_requests(self):

        yield Request(self.base_url, headers=self.headers,callback=self.parse_main_page)
    def parse_main_page(self, response):
        # print(response.text)
        html = response.text
        title = re.findall('title="(.*?)"',html)[0]
        print(title)

        # 提取视频信息
        info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        # info -> json字符串转成json字典
        json_data = json.loads(info)
        print("提取视频信息",json_data)
        # 提取视频链接
        video_url = json_data['data']['dash']['video'][2]['baseUrl']
        print("提取视频链接",video_url)
        # 提取音频链接
        audio_url = json_data['data']['dash']['audio'][2]['baseUrl']
        print("提取音频链接",audio_url)

        # for i in

        video_content = requests.get(url=video_url, headers=self.headers).content
        # 获取音频内容
        audio_content = requests.get(url=audio_url, headers=self.headers).content
        # 保存数据
        with open('video/' + title + '.mp4', mode='wb') as v:
            v.write(video_content)
        with open('video/' + title + '.mp3', mode='wb') as a:
            a.write(audio_content)

