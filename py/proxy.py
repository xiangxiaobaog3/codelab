import requests

proxies = {
    "http": "http://10.1.231.47:8083",
}

r = requests.get("http://g.cn", proxies=proxies)
r = requests.get("https://www.google.com", proxies=proxies)
print(r.text)

# 172.16.232.93
