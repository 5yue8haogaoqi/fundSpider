from urllib import request,parse


test_html_save_path = '/Users/Fiona/github/blogs/'

#爬虫对应的网址
spider_url_path = 'https://www.howbuy.com/fund/ajax/fundranking/index.htm'



def getRequestResult(params, url=spider_url_path):
    post_params = parse.urlencode(params)
    post_params = post_params.encode()
    with request.urlopen(url, data=post_params) as f:
        b = f.read()
        content = b.decode('utf-8')
        return content

def select_gupiao():
    #构建post参数
    params = Parameters()
    for p,ind in params:
        re = getRequestResult(p)
        with open(test_html_save_path+ind+'.html', mode='w') as f:
            f.write(re)


def select_zhiaquan():
    pass

def search_topN(topN=20):
    """
    根据正则匹配topN的基金的代码
    :param topN: 默认返回top20的基金代码LIST
    :return: LIST, for example ['1120','1103'...]
    """



class Parameters(object):

    def __init__(self):
        self._variation = ['hb1z','hb1y','hb3y','hb6y','hb1n','hbjn']

    def __iter__(self):
        return  self

    def __next__(self):
        try:
            params = [('glrm', ''), ('keyword', ''), ('radio', ''), ('bd', ''), ('ed', ''), ('orderType', 'desc')]
            p0 = self._variation.pop()
            p1 = ['orderField']
            p1.append(p0)
            p1 = tuple(p1)
            p2 = ('cat', 'gupiao.htm')
            params.append(p1)
            params.append(p2)
            return params, p0
        except:
            raise StopIteration


if __name__ == '__main__':
    select_gupiao()