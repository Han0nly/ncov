# -*- coding: utf-8 -*-
"""
@Time        : 2020/7/19 12:25
@Author      : NingWang
@Email       : yogehaoren@gmail.com
@File        : Utils.py
@Description :
@Version     : 0.1-dev
@Edited      : Xiaohan
"""
import requests
import pickle
import json

DEFAULT_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64",
    "X-Requested-With": "XMLHttpRequest",
}

UPLOAD_HEADER = {
    "Referer": "https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup",
    "Origin": "https://xxcapp.xidian.edu.cn",
}

NORTH_UPLOAD_MESSAGE = {
    "geo_api_info": "{\"type\":\"complete\",\"info\":\"SUCCESS\",\"status\":1,\"VDa\":\"jsonp_324977_\",\"position\":{\"Q\":34.23254,\"R\":108.91516000000001,\"lng\":108.91800,\"lat\":34.23230},\"message\":\"Get ipLocation success.Get address success.\",\"location_type\":\"ip\",\"accuracy\":null,\"isConverted\":true,\"addressComponent\":{\"citycode\":\"029\",\"adcode\":\"610113\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"白沙路\",\"streetNumber\":\"付8号\",\"country\":\"中国\",\"province\":\"陕西省\",\"city\":\"西安市\",\"district\":\"雁塔区\",\"township\":\"电子城街道\"},\"formattedAddress\":\"陕西省西安市雁塔区电子城街道西安电子科技大学北校区\",\"roads\":[],\"crosses\":[],\"pois\":[]}",
    "area": "陕西省 西安市 雁塔区",  # 地区
    "city": "西安市",  # 城市
    "province": "陕西省",  # 省份
    "address": "陕西省西安市雁塔区电子城街道西安电子科技大学北校区",  # 实际地址
}

SOUTH_UPLOAD_MESSAGE = {
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":34.121994628907,\"R\":108.83715983073,\"lng\":108.83716,\"lat\":34.121995},\"location_type\":\"html5\",\"message\":\"Get ipLocation failed.Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"029\",\"adcode\":\"610116\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"雷甘路\",\"streetNumber\":\"264号\",\"country\":\"中国\",\"province\":\"陕西省\",\"city\":\"西安市\",\"district\":\"长安区\",\"township\":\"兴隆街道\"},\"formattedAddress\":\"陕西省西安市长安区兴隆街道西安电子科技大学长安校区办公辅楼\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "陕西省 西安市 长安区",  # 地区
    "city": "西安市",  # 城市
    "province": "陕西省",  # 省份
    "address": "陕西省西安市长安区兴隆街道西安电子科技大学长安校区行政辅楼",  # 实际地址
}

HOME_UPLOAD_MESSAGE = {
    "address": "山东省青岛市即墨区潮海街道埠惜路金盟山庄",
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":36.405007052952,\"R\":120.51044216579902,\"lng\":120.510442,\"lat\":36.405007},\"location_type\":\"html5\",\"message\":\"Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"0532\",\"adcode\":\"370215\",\"businessAreas\":[{\"name\":\"即墨\",\"id\":\"370215\",\"location\":{\"Q\":36.388599,\"R\":120.453079,\"lng\":120.453079,\"lat\":36.388599}}],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"流浩河三路\",\"streetNumber\":\"2号\",\"country\":\"中国\",\"province\":\"山东省\",\"city\":\"青岛市\",\"district\":\"即墨区\",\"township\":\"潮海街道\"},\"formattedAddress\":\"山东省青岛市即墨区潮海街道埠惜路金盟山庄\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "山东省 青岛市 即墨区",
    "province": "山东省",
    "city": "青岛市",
}

LOGIN_URL = "https://xxcapp.xidian.edu.cn/uc/wap/login/check"
COOKIE_FILE_NAME = "cookie.txt"


def get_cookie_from_login(student_id: str, password: str, cookie_file_path: str):
    """
    登录获取cookie
    :param student_id: 学号
    :param password:  密码
    :param cookie_file_path cookies文件路径
    :return:
    """
    r = requests.post(LOGIN_URL, data={"username": student_id, "password": password}, headers=DEFAULT_HEADER)
    if r.status_code == 200:
        if r.json()['e'] == 0:
            print("登录成功")
            with open(cookie_file_path, 'wb') as f:
                pickle.dump(r.cookies, f)
        else:
            print(r.json()['m'])
            raise RuntimeError("登录失败, 请检查用户名或密码是否正确")


def load_cookie_from_file(cookie_file_path: str):
    """
    从文件中加载cookie
    :param cookie_file_path: 文件路径
    :return:
    """
    with open(cookie_file_path, 'rb') as f:
        return pickle.load(f)


def load_upload_message_file(file_path: str, location: str):
    """
    从文件中解析需要提交的信息
    :param file_path: 文件路径
    :return:
    """
    with open(file_path, "r", encoding='utf8') as f:
        # 这里用eval来处理json，因为josn库无法解析带有注释的json文件
        text = f.read()
        # upload_message = json.load(f)
        upload_message = eval(text)
        if location == "s":
            for key, value in SOUTH_UPLOAD_MESSAGE.items():
                if key not in upload_message:
                    upload_message[key] = value
            return upload_message
        elif location == "n":
            for key, value in NORTH_UPLOAD_MESSAGE.items():
                if key not in upload_message:
                    upload_message[key] = value
            return upload_message
        elif location == "home":
            for key, value in HOME_UPLOAD_MESSAGE.items():
                if key not in upload_message:
                    upload_message[key] = value
            return upload_message


def upload_ncov_message(url, cookie, upload_message):
    header = dict(DEFAULT_HEADER.items() | UPLOAD_HEADER.items())
    r = requests.post(url, upload_message, cookies=cookie, headers=header, )
    if r.json()['e'] == 0:
        print("上报成功")
    else:
        print("上报出现错误!")
        print("错误信息: ", r.json()['m'])
