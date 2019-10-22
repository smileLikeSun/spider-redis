import requests
from bs4 import BeautifulSoup
import re

def get_proxy():
    ip_list = []
    with open('proxy.txt', 'r') as fi:
        ips = fi.readlines()
        for ip in ips:
            ip = ip.split('\n')[0]
            ip_list.append(ip)
    return ip_list



def get_ips():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWYxOWZjYTUyZTE1Y2JmZDZhMGNmZDlkY2E5ZDE0MjNhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVg1cmI5WURSQ0grdDViQkpDVW5jMjAwVFE4cS9nRWNUTzVtajJreVVlRlk9BjsARg%3D%3D--0e05d0fed8ada6ded81af315b4cf8d8cf0ff9734; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1570850446; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1570850446',
        'Host': 'www.xicidaili.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    url_bilibili = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=67456873&sort=2'
    url_proxy = 'https://www.xicidaili.com/wn/{}'
    process_totle = 200
    process_count = 1
    process_line = ''
    print('[{:-<20}]'.format(process_line))
    with open(f'../proxy.txt', 'w', encoding='utf-8') as fi:
        for i in range(1, 3):
            url_proxy = url_proxy.format(i)
            content = requests.get(url_proxy, headers=headers)
            res = content.text
            soup = BeautifulSoup(res, 'lxml')
            td_list = soup.table.children
            for tr in td_list:
                ip = re.findall('<td>(\d+[.]\d+[.]\d+[.]\d+)</td>', str(tr))
                port = re.findall('<td>(\d+)</td>', str(tr))
                if len(ip):
                    host = '{}:{}'.format(ip[0], port[0])
                    proxies = {
                        'http': 'http://' + host,
                        'https': 'https://' + host,
                    }
                    try:
                        response = requests.get(url_bilibili, proxies=proxies, timeout=1)
                        if response.status_code == 200:
                            print(host)
                            fi.write('https://{}\n'.format(host))
                    except Exception:
                        print('the ip:{} not to use'.format(host))
                    finally:
                        if process_count % 10 == 0:
                            process_line += '*'
                            print('[{:-<20}]'.format(process_line))
                        process_count += 1


if __name__ == '__main__':
    get_ips()
    # get_proxy()
