from urllib import request,parse


html_save_path = '/Users/Fiona/github/blogs/test.html'
url_path = 'https://www.howbuy.com/fund/ajax/fundranking/index.htm'
params = [('glrm',''),('keyword',''),('radio',''),('bd',''),('ed',''),('orderField','hb3y'),('orderType','desc'),('cat','gupiao.htm')]

post_params = parse.urlencode(params)
post_params = post_params.encode(encoding='utf-8')
with request.urlopen(url_path, data=post_params) as f:
    bytes = f.read()
    conent = bytes.decode('utf-8')

    with open(html_save_path, mode='w', encoding='utf-8') as h:
        h.write(conent)


