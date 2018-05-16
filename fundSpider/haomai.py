from urllib import request,parse
import re
import datetime


#爬虫对应的网址
spider_url_path = 'https://www.howbuy.com/fund/ajax/fundranking/index.htm'
type_gupiao = 'stock'
type_zhaiquan = 'bond'
type_hunhe = 'hunhe'
type_zhishu = 'zhishu'


def getRequestResult(params, url=spider_url_path):
    post_params = parse.urlencode(params)
    post_params = post_params.encode()
    with request.urlopen(url, data=post_params) as f:
        b = f.read()
        content = b.decode('utf-8')
        return content

def get_intersection(vList):
    """
    查看list中的每个list的交集
    :param vList:
    :return: 共同元素组成的list
    """
    intersaction = set()
    for i,val in enumerate(vList):
        if i == 0:
            intersaction = set(val)
        else:
            intersaction = intersaction & set(val)
    return intersaction


def select_in_topN(type,topN=20):
    """
    从topN中获取合适的基金
    :param type: 基金的类型，股票或债券，具体值在模块顶部定义了常量
    :param topN:
    :return:
    """
    #构建post参数
    params = Parameters(type)
    fundL = list()
    for p,ind in params:
        result= getRequestResult(p)
        # with open(test_html_save_path+ind+'.html', mode='w') as f:
        #     f.write(result)
        codeL = regex_topN(result,topN)
        fundL.append(codeL)
    return fundL,get_intersection(fundL)

def regex_topN(html_content,topN=20):
    """
    根据正则匹配topN的基金代码，包含隐藏的部分
    :param html_content:
    :param topN:
    :return:
    """
    html_content = html_content.replace('\t','')
    html_content = html_content.replace('\r','')
    html_content = html_content.replace('\n','')
    html_content = html_content.replace(' ','')

    regex_str =r'/fund/(\d{6})'
    pattern = re.compile(regex_str)
    result = re.finditer(pattern, html_content)
    codeList = list()
    for element in result:
        fund_code = element.group(1)
        if fund_code in codeList:
            continue
        codeList.append(fund_code)
        if len(codeList) == topN:
            break
    return codeList


def search_topN(html_content,topN=20):
    """
    根据正则匹配topN的基金的代码
    :param topN: 默认返回top20的基金代码LIST
    :return: LIST, for example ['1120','1103'...]
    """
    html_content = html_content.replace('\t','')
    html_content = html_content.replace('\r','')
    html_content = html_content.replace('\n','')
    html_content = html_content.replace(' ','')
    regex_str = r'<table.*><tbody>(.*)</tbody></table>'
    pattern = re.compile(regex_str)
    result = re.match(pattern, html_content)

    regex_code = r'>(\d{6})<'
    pattern = re.compile(regex_code)
    code_iter = pattern.finditer(result.group(1))
    codeL = list()
    for code in code_iter:
        codeL.append(code.group(1))
    codeNum = len(codeL)
    if codeNum < topN :
        print ('你设定的数量超过返回结果，请重新确认')
        return []
    return codeL[0:topN]

class Parameters(object):

    def __init__(self,type):
        self._variation = ['hb1z','hb1y','hb3y','hb6y','hb1n','hbjn','hbRange']
        self._type = type

    def _getp2(self):
        if(self._type == type_gupiao):
            return ('cat', 'gupiao.htm')
        if(self._type == type_zhaiquan):
            return ('cat', 'zhaiquan.htm')
        if(self._type == type_hunhe):
            return ('cat', 'hunhe.htm')
        if(self._type == type_zhishu):
            return ('cat', 'zhishu.htm')


    def __iter__(self):
        return  self

    def __next__(self):
        try:
            params = [('glrm', ''), ('keyword', ''), ('radio', ''), ('orderType', 'desc')]
            p0 = self._variation.pop()
            p1 = ['orderField']
            p1.append(p0)
            p1 = tuple(p1)
            p2 = self._getp2()
            params.append(p1)
            params.append(p2)
            """
            hbRange说明是动态时间的参数，bd和ed这两个参数有变化
            """
            if p0 == 'hbRange':
                params.extend(self.get_date_parameter(True))
            else:
                params.extend(self.get_date_parameter())
            return params, p0
        except:
            raise StopIteration

    def _current_date(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d')

    def _three_year_ago(self):
        now = datetime.datetime.now()
        year = now.year
        month =now.month
        day = now.day
        result_format ='{}-{}-{}'
        return result_format.format((int(year)-3),month,day)

    def get_date_parameter(self,ifNeedValue=False):
        """
        获取时间类型的参数
        :return:
        """
        if ifNeedValue:
            return [('bd',self._three_year_ago()),('ed',self._current_date())]
        return [('bd', ''), ('ed', '')]

if __name__ == '__main__':
    fundL,intersection = select_in_topN(type_zhaiquan, 100)
    print (intersection)
    # p = Parameters(type_zhaiquan)
    # for params,ind in p:
    #     content  = getRequestResult(params, spider_url_path)
        # save_file_path = 'D:\\{}.html'
        # with open(save_file_path.format(ind), mode='w') as f:
        #     f.write(content)