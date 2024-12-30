# import json
# info = 'test.json'
#
# # 打开文件并读取内容
# with open(info, 'r', encoding='utf-8') as file:
#     data = file.read()
#
#     # 解析读取的JSON字符串
#     json_data = json.loads(data)
#
#     print(len(json_data['data']['dash']['video']))
#     print("提取视频信息", json_data['data']['dash']['video'])

# 导入数据请求模块
import requests
# 导入正则表达式模块
import re
# 导入json模块
import json
# TODO 记得更改你要的url和你自己的cookie
url = 'https://www.bilibili.com/video/BV1xD6MYGEzD/?vd_source=37c354da4828eaabf7648c9912199f9a'
cookie="buvid3=728DF2A2-7F59-F5D3-3E33-529CFAECEF3C91689infoc; b_nut=1727425491; _uuid=F126631E-1087D-10D87-EB74-294CA6E586CA91995infoc; buvid4=7BEE92FF-6B7A-48AA-506C-15BE3F67C22992679-024092708-TMpdmdQTOL0eld9TU91%2F9g%3D%3D; buvid_fp=36bb8831f81dd2bdcb4c384bc477126a; rpdid=|(J|YJkm)RYY0J'u~k~RklRmR; header_theme_version=CLOSE; enable_web_push=DISABLE; home_feed_column=5; DedeUserID=18516237; DedeUserID__ckMd5=36d9a216a28eecbf; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzU1NDY4MzcsImlhdCI6MTczNTI4NzU3NywicGx0IjotMX0.jEoVt53D59isS7cc897s7hKsWnlyg54f56nnZONWAt8; bili_ticket_expires=1735546777; SESSDATA=2aecc8be%2C1750839657%2Cf1fa1%2Ac1CjAI1qZw_5a5F_aQUcxWOdJ54WTJbj1BlVvcfUQRmZVJXopt3NgKx8b1g3F6yq4CNF4SVmFUVlkwVWxWNmFMSXZ5eHpZRlNaZ1p6ajVjMlpHcHMxM3dtOGJXRHdxUGJDWUMwcE90VDVBRC0yVjlmd2FDRTEzNUNZSnNiMC1oUHZYcDFCRjdiSk9BIIEC; bili_jct=09b072b4f6a88c42b4939e6ad38e1ce1; sid=82twx2c0; bp_t_offset_18516237=1015543810253389824; b_lsid=2610D10424_1941513281C; bsource=search_bing; browser_resolution=1492-848; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; CURRENT_FNVAL=4048"
headers = {
        # Referer 防盗链
        "Referer": url,
        # User-Agent 用户代理, 表示浏览器/设备基本身份信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Cookie": cookie
}
# 发送请求
response = requests.get(url=url, headers=headers)
html = response.text
print(html)
# 解析数据: 提取视频标题
title = re.findall('title="(.*?)"', html)[0]
print(title)
# 提取视频信息
info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
p_index_p = re.findall('window.__INITIAL_STATE__=(.*?);', html)[0]
# info -> json字符串转成json字典
# print("分级信息",p_index_p)
json_data = json.loads(info)

print("视频信息",json_data['data']['dash']['video'])
p_json_data = json.loads(p_index_p)
print('分P信息',p_json_data["availableVideoList"][0]["list"])
# # 提取视频链接

video_url = json_data['data']['dash']['video'][0]['baseUrl']
print(video_url)
# 提取音频链接
audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
print(audio_url)
# video_content = requests.get(url=video_url, headers=headers).content
# # 获取音频内容
# audio_content = requests.get(url=audio_url, headers=headers).content
# # 保存数据
# with open('video\\' + title + '.mp4', mode='wb') as v:
#     v.write(video_content)
# with open('video\\' + title + '.mp3', mode='wb') as a:
#     a.write(audio_content)

import moviepy
# from moviepy.editor import VideoFileClip, AudioFileClip

# 加载视频文件
video = moviepy.VideoFileClip("python游戏】10款Python小游戏案例（附源码教程）一天学一个，边玩游戏边学习.mp4")

# 加载音频文件
audio = moviepy.AudioFileClip("python游戏】10款Python小游戏案例（附源码教程）一天学一个，边玩游戏边学习.mp3")

# 将音频设置到视频上
video_with_audio = video.with_audio(audio)

# 输出新的视频文件
video_with_audio.write_videofile("output_with_audio.mp4", codec="libx264",
                                 audio_codec="aac",
                                 preset='ultrafast',  # 尝试更快的预设
                                 threads=4)