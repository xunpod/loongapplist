# coding=utf-8
import json
import pandas as pd
import requests


def get_last_app_info():
    url = "http://113.24.212.22:8080/community/app/latests"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                      "Safari/537.36 Edg/120.0.0.0",
    }
    data = {
        "page": 1,
        "per_page": 1
    }
    res = requests.post(url, headers=headers, json=data)
    dict_temp = json.loads(res.text)
    dict_temp = dict_temp["data"]
    total = dict_temp["total"]
    dict_temp = dict_temp["vodata"]
    last_app_info = pd.DataFrame(dict_temp)
    return last_app_info, total, res.text


def get_all_app_info():
    # 获取所有app的信息，开发者信息和app详情页地址需另行获取
    url = "http://113.24.212.22:8080/community/app/latests"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                      "Safari/537.36 Edg/120.0.0.0",
    }
    data = {
        "page": 1,
        "per_page": get_last_app_info()[1]
    }
    res = requests.post(url, headers=headers, json=data)
    dict_temp = json.loads(res.text)
    dict_temp = dict_temp["data"]
    dict_temp = dict_temp["vodata"]
    df_app_info = pd.DataFrame(dict_temp)
    # 获取开发者信息 & app详情页地址
    url_first = "http://app.loongapps.cn/#/detail/"
    url_list = []
    dev_list = []
    for app_id in df_app_info["id"]:
        url = "http://113.24.212.22:8080/community/app"
        data = {"process": "INFO", "id": app_id}
        res = requests.post(url, headers=headers, json=data)
        dict_temp = json.loads(res.text)
        dict_temp = dict_temp["data"]
        app_url = url_first + str(app_id)
        url_list.append(app_url)
        dev_list.append(dict_temp["developerName"])
    df_dev_list = pd.DataFrame(dev_list)
    df_url_list = pd.DataFrame(url_list)
    # 构造完整信息
    df_app_info["developerName"] = df_dev_list
    df_app_info["appUrl"] = df_url_list
    app_data = []
    df_app_data = pd.DataFrame(app_data)
    df_app_data["应用编号"] = df_app_info["id"]
    df_app_data["应用名称"] = df_app_info["name"]
    df_app_data["页面链接"] = df_app_info["appUrl"]
    df_app_data["版本号"] = df_app_info["version"]
    df_app_data["下载链接"] = df_app_info["downloadUrl"]
    df_app_data["文件大小"] = df_app_info["appSize"]
    df_app_data["应用类型"] = df_app_info["categoryName"]
    df_app_data["开发者"] = df_app_info["developerName"]
    df_app_data["更新时间"] = df_app_info["updateTime"]
    df_app_data["图片链接"] = df_app_info["logoUrl"]
    df_app_data["可执行文件"] = df_app_info["exec"]
    # 写入csv
    df_app_data.to_csv("loongapplist-latest.csv", encoding='utf-8-sig', index=False)

df_latest_app= pd.read_csv("loongapplist-latest.csv", encoding="utf-8-sig")
if df_latest_app["应用编号"][0]==get_last_app_info()[0]["id"][0] and df_latest_app["应用名称"][0]==get_last_app_info()[0]["name"][0] and df_latest_app["版本号"][0]==get_last_app_info()[0]["version"][0]:
    print("当前数据已是最新")
else:
    get_all_app_info()


