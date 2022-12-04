import requests
import os
from bs4 import BeautifulSoup
import shutil
import copy

get = requests.get
head = requests.head

def complete_url(url):
    if len(url) > 0:
        if url[:2] == '//':
            url = 'http:' + url
        elif url[:3] == 'www':
            url = 'http://' + url
    return url

def req_url(url, req_type=get):
    try:
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
        }
        res = req_type(url, headers=headers)
        res.encoding = res.apparent_encoding
        return res
    except:
        return None
    

def resolve_html(res):
    if os.path.exists('Images'):
        shutil.rmtree('Images')
    os.makedirs('Images')
    
    soup = BeautifulSoup(res.content,'html.parser')
    soupall = soup.find_all()
    
    text_names = ['h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','p']
    avai_elements = []
    for item in soupall:
        # capture hyperlink
        if item.name == 'a' and item.string is not None and item.get("href") is not None:
            avai_elements.append({'type':'hyperlink', 'string':item.string, 'href':complete_url(item['href'])})
        # capture text
        elif item.name in text_names and item.string is not None and item.string != '':
            avai_elements.append({'type':'text', 'string':item.string})
        # capture images
        elif 'img' in item.name:
            h, s = item.get("href"), item.get("src")
            src = h if h is not None else(s if s is not None else None)
            if 'png' in src or 'jpeg' in src or 'jpg' in src:
                img_url = complete_url(src)
                img_name = img_url.split('/')[-1][-10:].replace('?','_')
                img_res = req_url(img_url)
                if True in [img_url == e['url'] for e in avai_elements if e['type'] == 'image']: continue
                if img_res is not None:
                    with open(f'Images/{img_name}','wb') as f:
                        f.write(img_res.content)  
                        avai_elements.append({'type':'image', 'url':img_url, 'path':f'Images/{img_name}'})
    
    
    ae_copy = []
    for e in avai_elements:
        if e['type'] == 'text' and (True in [e['string'] == e2['string'] for e2 in avai_elements if e2['type'] in ['hyperlink']]):
            continue
        # if e['type'] == 'image' and (True in [e['url'] == e2['url'] for e2 in ae_copy if e2['type'] in ['image']]):
        #     continue
        ae_copy.append(e)
    
    return ae_copy


def trans2html(avai_elements):
    all_html = ''
    for e in avai_elements:
        if e['type'] == 'hyperlink':
            all_html += f'<a href={e["href"]}> {e["string"]}</a>'
        elif e['type'] == 'text':
            all_html += f'<p> {e["string"]} </p>'
        elif e['type'] == 'image':
            all_html += f'<img src="{e["path"]}">'
    return all_html

def dict2html(s,g):
    all_html = '<h3> 发送命令头部 </h3>'
    for k,v in s.items():
        all_html += f'<p> <b>{k}</b>: {v}</p>'
    all_html += '<h3>___________________________</h3> <h3> 接收响应头部 </h3>'
    for k,v in g.items():
        all_html += f'<p> <b>{k}</b>: {v}</p>'
    return all_html
    
if __name__ == '__main__':
    urls = [
    'https://meiriyiwen.com/',
    'https://www.baidu.com/',
    'https://www.douban.com/',
    'https://www.cnblogs.com/tiannuo/articles/15563241.html',
    'https://www.cnblogs.com/tiannuo/p/15963788.html',
    'https://zhuanlan.zhihu.com/p/84316213',
    'http://tieba.baidu.com/f?fr',
    ]
    res = req_url(url=urls[-1])
    print(res.text)
    avai_elements = resolve_html(res)
    # print(dict2html(res.request.headers,res.headers))
    # for i in avai_elements:
    #     print(i)

