from urllib import request,parse


test_html_save_path = 'D:\\note\\markdown\\test.html'

#爬虫对应的网址
spider_url_path = 'https://www.howbuy.com/fund/ajax/fundranking/index.htm'
#待post传入的参数，需要替换orderField后面的占位符的参数
params = [('glrm',''),('keyword',''),('radio',''),('bd',''),('ed',''),('orderType','desc')]



def getRequestResult(params, url=spider_url_path):
    post_params = parse.urlencode(params)
    post_params = post_params.encode(encoding='utf-8')
    with request.urlopen(url, data=post_params) as f:
        b = f.read()
        content = b.decode('utf-8')
        return content

def select_gupiao():
    #构建post参数
    p1 = ('orderField','hb1z')
    p2 = ('cat','gupiao.htm')
    p = list()
    p.extend(params)
    p.extend(p1)
    p.extend(p2)

    re = getRequestResult(p)
    with open(test_html_save_path, mode='w', encoding='urf-8') as f:
        f.write(re)

def select_zhiaquan():
    pass


if __name__ == '__main__':
    select_gupiao()