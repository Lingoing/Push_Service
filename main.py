import json
import time
from binascii import hexlify
from urllib.parse import quote

import requests
from Cryptodome.Hash import SHA1


def get_session():
    headers = {
        "Host": "bjcloudpayment.cebbank.com",
        "Accept": "*/*",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9"
                         ".eyJzdWIiOiI4YzA3OTNhOWZkM2M0YWI5OWU5OTI1YTM3OWE4NDljZiIsImlhdCI6MTY3OTkwMTUxNCwiZXhwIjoxNjc5OTA4NzE0fQ.BzoQ9t5MjkL-N28TbTm5sBylbEiN37IaKg_9QoZSSqGGetfjIVmebOTe7Axptsi6LqHA0ZFcZ0e8hWBZPDsOhg",
        "Accept-Charset": "utf-8",
        "Accept-Language": "zh-CN,en-US;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=utf-8",
        "Content-Length": "43",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/20D67 Ariver/1.1.0 AliApp(AP/10.3.66.6000) Nebula WK RVKType(0) "
                      "AlipayDefined(nt:4G,ws:390|780|3.0,ac:T|ss) AlipayClient/10.3.66.6000 Language/zh-Hans "
                      "Region/CN NebulaX/1.0.0 XRiver/10.2.58.1",
        "Referer": "https://2021002147635087.hybrid.alipay-eco.com/2021002147635087/0.2.2303221653.12/index.html"
                   "#pages/index/transferPage/index",
        "alipayMiniMark": "JcFk83uVJ7R7/NA7x8FSozgPjUdjw+pid34Ge2ke89jDbKDkJeltt613caLWjtoPwz"
                          "+v6lcKayIyCdBwTyddYlSMqF0jyL5P4J2+I8qThGs=",
        "Connection": "keep-alive",
        "x-ceb-cloudpayment-adcode": "370700"
    }
    cookies = {
        "JSESSIONID": "63C1FCC63197E37F3B60EE7EDF858161"
    }
    url = "https://bjcloudpayment.cebbank.com/ceb-bf-cloud-payment/webapi/item/queryBillInformation"
    data = {
        "companyId": "010026653",
        "billKey": "93230"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    return response.text


def get_balance():
    headers = {
        "Host": "bjcloudpayment.cebbank.com",
        "Accept": "*/*",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9"
                         ".eyJzdWIiOiI4YzA3OTNhOWZkM2M0YWI5OWU5OTI1YTM3OWE4NDljZiIsImlhdCI6MTY3OTkwMTUxNCwiZXhwIjoxNjc5OTA4NzE0fQ.BzoQ9t5MjkL-N28TbTm5sBylbEiN37IaKg_9QoZSSqGGetfjIVmebOTe7Axptsi6LqHA0ZFcZ0e8hWBZPDsOhg",
        "Accept-Charset": "utf-8",
        "Accept-Language": "zh-CN,en-US;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=utf-8",
        "Content-Length": "34",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/20D67 Ariver/1.1.0 AliApp(AP/10.3.66.6000) Nebula WK RVKType(0) "
                      "AlipayDefined(nt:4G,ws:390|780|3.0,ac:T|ss) AlipayClient/10.3.66.6000 Language/zh-Hans "
                      "Region/CN NebulaX/1.0.0 XRiver/10.2.58.1",
        "Referer": "https://2021002147635087.hybrid.alipay-eco.com/2021002147635087/0.2.2303221653.12/index.html"
                   "#pages/index/transferPage/index",
        "alipayMiniMark": "JcFk83uVJ7R7/NA7x8FSo7LotPY0AqriTlWVxbCZPIWILg1OO9nB5G0DFf6jVuuDeG7M+VH8ktlLAm"
                          "+S3NijNVGxbuWUlmhmFjri4ic+gik=",
        "Connection": "keep-alive",
        "x-ceb-cloudpayment-adcode": "370700"
    }
    cookies = {
        "JSESSIONID": "A78A28BAC4AA2F7AB0AD37A4BE8C4F6F"
    }
    url = "https://bjcloudpayment.cebbank.com/ceb-bf-cloud-payment/webapi/item/queryBillInformationDetail"
    data = {
        "trmSeqNum": str(json.loads(get_session())['data']['trmSeqNum'])
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    return response.text


def temp_function():
    bark_url = 'https://api.day.app/TbsfqDZZoJXnaP46cttdsN/'
    json_data = json.loads(get_balance())
    print(json_data)
    if json_data['ret_code'] != 0:
        requests.get(
            f'{bark_url}数据获取失败！')
    else:
        balance = json_data['data'][0]['balance']
        if balance < 2000:
            requests.get(
                f'{bark_url}水费余额不足，请及时充值！\n当前余额：{balance / 100}元')
        else:
            print(f'当前余额：{balance / 100}元')


def generate_device_id():
    h = hexlify(SHA1.new(str(time.time_ns()).encode('ascii')).digest()).decode('ascii')
    return "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:32])


def get_response(device_id='DE233B26-4B37-46B9-A82B-84ECEA93DFCC', location='119.206905,36.721429'):
    url = f'https://wrapper.cyapi.cn/v2.6/UR8ASaplvIwavDfR/{location}/weather?lang=zh_CN&dailystart=-1&hourlysteps' \
          f'=384&dailysteps=16&alert=true&device_id={device_id}&upload_event_key=main_weather_api_error&upload_fail=1'
    response = requests.get(url)
    return response.text


def get_aqi(aqi_number):
    if aqi_number >= 0:
        if aqi_number in range(0, 51):
            return '优'
        elif aqi_number in range(51, 101):
            return '良'
        elif aqi_number in range(101, 151):
            return '轻度'
        elif aqi_number in range(151, 201):
            return '中度'
        elif aqi_number in range(201, 301):
            return '重度'
        else:
            return '严重'


def get_weather_type(sky_con):
    print(sky_con)
    if sky_con == 'CLEAR_DAY':
        return '晴朗'
    elif sky_con == 'CLEAR_NIGHT':
        return '晴朗'
    elif sky_con == 'PARTLY_CLOUDY_DAY':
        return '多云'
    elif sky_con == 'PARTLY_CLOUDY_NIGHT':
        return '多云'
    elif sky_con == 'CLOUDY':
        return '阴'
    elif sky_con == 'CLOUDY_NIGHT':
        return '阴'
    elif sky_con == 'RAIN':
        return '雨'
    elif sky_con == 'SNOW':
        return '雪'
    elif sky_con == 'SNOW_NIGHT':
        return '雪'
    elif sky_con == 'WIND':
        return '风'
    elif sky_con == 'FOG':
        return '雾'
    elif sky_con == 'HAZE':
        return '霾'
    elif sky_con == 'LIGHT_HAZE':
        return '雾霾'
    elif sky_con == 'SLEET':
        return '冻雨'
    elif sky_con == 'DUST':
        return '浮尘'
    else:
        return '未知'


def get_wind_direction(angle):
    if angle >= 337.5 or angle < 22.5:
        return "北风"
    elif 22.5 <= angle < 67.5:
        return "东北风"
    elif 67.5 <= angle < 112.5:
        return "东风"
    elif 112.5 <= angle < 157.5:
        return "东南风"
    elif 157.5 <= angle < 202.5:
        return "南风"
    elif 202.5 <= angle < 247.5:
        return "西南风"
    elif 247.5 <= angle < 292.5:
        return "西风"
    else:
        return "西北风"


def get_wind_scale(wind_speed):
    wind_speed = round(wind_speed / 3.6, 1)
    print(wind_speed)
    if 0.0 <= wind_speed <= 0.2:
        return "0级无风(静，烟直上)"
    elif 0.3 <= wind_speed <= 1.5:
        return "1级软风(烟示风向)"
    elif 1.6 <= wind_speed <= 3.3:
        return "2级轻风(静，烟直上)"
    elif 3.4 <= wind_speed <= 5.4:
        return "3级微风(旌旗展开)"
    elif 5.5 <= wind_speed <= 7.9:
        return "4级和风(吹起尘土)"
    elif 8.0 <= wind_speed <= 10.7:
        return "5级劲风(小树摇摆)"
    elif 10.8 <= wind_speed <= 13.8:
        return "6级强风(电线有声)"
    elif 13.9 <= wind_speed <= 17.1:
        return "7级疾风(步行困难)"
    elif 17.2 <= wind_speed <= 20.7:
        return "8级大风(折毁树枝)"
    elif 20.8 <= wind_speed <= 24.4:
        return "9级烈风(小损房屋)"
    elif 24.5 <= wind_speed <= 28.4:
        return "10级狂风(拔起树木)"
    elif 28.5 <= wind_speed <= 32.6:
        return "11级暴风(摧毁重大)"
    elif 32.7 <= wind_speed <= 36.9:
        return "12级飓风(摧毁极大)"
    else:
        return "躺平吧，没救了！"



def get_text_api():
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "dnt": "1",
    "origin": "https://chp.shadiao.pro",
    "referer": "https://chp.shadiao.pro/",
    "sec-ch-ua": "\"Chromium\";v=\"21\", \" Not;A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}
    response = requests.get('https://api.shadiao.pro/chp',headers=headers)
    chp = json.loads(response.text)
    return chp['data']['text']


def json_to_form(json_data):
    if not json_data:
        return None
    sky_con = f'''天气类型：{get_weather_type(str(json_data['result']['realtime']['skycon']))}''' + '\n'
    temperature_current = f'''当前温度：{str(round(json_data['result']['realtime']['temperature']))}℃''' + '\n'
    temperature = f'''温度：{str(round(json_data['result']['daily']['temperature'][1]['min']))}-{str(round(json_data['result']['daily']['temperature'][1]['max']))}℃''' + '\n'
    apparent_temperature = f'''体感温度：{str(round(json_data['result']['realtime']['apparent_temperature']))}℃''' + '\n'
    # cloudrate = f'''云量：{str((json_data['result']['realtime']['cloudrate']) * 100)}%''' + '\n'
    humidity = f'''湿度：{str(round(json_data['result']['realtime']['humidity'] * 100))}%''' + '\n'
    visibility = f'''能见度：{str(round(json_data['result']['realtime']['visibility']))}km''' + '\n'
    direction = f'''{get_wind_direction(json_data['result']['realtime']['wind']['direction'])}'''
    speed = f'''{direction}：{get_wind_scale(json_data['result']['realtime']['wind']['speed'])}''' + '\n'
    aqi = f'''AQI：{get_aqi(json_data['result']['realtime']['air_quality']['aqi']['chn'])}''' + '\n'
    ultraviolet = f'''紫外线强度：{json_data["result"]["realtime"]["life_index"]["ultraviolet"]["desc"]}''' + '\n'
    comfort = f'''舒适度：{json_data["result"]["realtime"]["life_index"]["comfort"]["desc"]}''' + '\n'
    forecast_keypoint = f'''预测：{json_data["result"]["forecast_keypoint"]}''' + '\n'

    title = '每日天气预报' + '\n\n'
    my_bark_url = 'https://api.day.app/TbsfqDZZoJXnaP46cttdsN/'
    her_bark_url = 'https://api.day.app/waz65gi8Cz3aWuZqCSBLfG/'

    if json_data['result']['alert']['content']:
        alert = json_data['result']['alert']['content'][0]['description'] + '\n\n'
        #requests.get(
        #    f'{my_bark_url}{quote(title + alert + sky_con + temperature_current + apparent_temperature + temperature + humidity + visibility + speed + aqi + ultraviolet + comfort + forecast_keypoint)}')
        requests.get(
            f'{her_bark_url}{quote(title + alert + sky_con + temperature_current + apparent_temperature + temperature + humidity + visibility + speed + aqi + ultraviolet + comfort + forecast_keypoint)}')
        time.sleep(5)
        #requests.get(my_bark_url + get_text_api())
        requests.get(her_bark_url + get_text_api())
    else:
        #requests.get(
        #    f'{my_bark_url}{quote(title + sky_con + temperature_current + apparent_temperature + temperature + humidity + visibility + speed + aqi + ultraviolet + comfort + forecast_keypoint)}')
        requests.get(
            f'{her_bark_url}{quote(title + sky_con + temperature_current + apparent_temperature + temperature + humidity + visibility + speed + aqi + ultraviolet + comfort + forecast_keypoint)}')
        time.sleep(5)
        #requests.get(my_bark_url + get_text_api())
        requests.get(her_bark_url + get_text_api())


if __name__ == '__main__':
    # my_location = ''
    # her_location = '119.1156110459953,36.74347502354077'
    # tai_shan = '117.094738,36.269893'
    # json_to_form(json.loads(get_response(generate_device_id(), her_location)))
    bark_url = 'https://api.day.app/TbsfqDZZoJXnaP46cttdsN/'
    json_data = json.loads(get_balance())
    errorCode = json_data['errorCode']
    if errorCode != 'AAAAAAA':
        print("获取余额信息失败！")
    else:
        balance = int(json_data['data']['billData'][0]['balance'])
        if balance <= 2000:
            requests.get(
                f'{bark_url}水费余额不足，请及时充值！\n当前余额：{balance / 100}元')
            print(f'通知已发送，当前余额：{balance / 100}元')
        else:
            requests.get(
                f'{bark_url}当前余额：{balance / 100}元')
            print(f'当前余额：{balance / 100}元')
