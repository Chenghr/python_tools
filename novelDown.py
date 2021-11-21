"""
python 爬虫系列，下载小说保存为 txt
"""
import re
import requests
from bs4 import BeautifulSoup

# 根据不同的网页，写不同的正则表达式匹配
findTitle = re.compile(r'<h1 class="bookname">(.*?)<small>',re.S)
findText = re.compile(r'<p>(.*?)</p>',re.S)
findLinkTemp = re.compile(r'<a href="(.*?)" id="next_url" rel="next">下一页</a>')
findLinkNextChap = re.compile(r'<a href="(.*?)" id="next_url" rel="next">下一章</a>')

class downloader(object):

    def __init__(self, base_url, txt_path):
        self.base_url = base_url  # 小说起始页
        self.txt_path = txt_path  # 小说存储位置

    def get_soup(self, url):
        req = requests.get(url = url)
        req.encoding = req.apparent_encoding
        soup = BeautifulSoup(req.text, 'html.parser')

        return soup

    def get_next_url(self, soup, tag):
        """
        tag=0返回下一页的url；tag=1则返回下一章的url
        """
        url = ''
        for item in soup.find_all('div',class_="bottem2"):
            item = str(item)
            if tag == 0:
                # 下一页
                link = re.findall(findLinkTemp, item)[0]
            else:
                # 下一章
                link = re.findall(findLinkNextChap, item)[0]
            url = self.base_url + str(link)
        
        return url

    def get_title(self, soup):
        # 获取一章的标题
        for item in soup.find_all('h1',class_="bookname"):
            item = str(item)
            print(item)
            title = re.findall(findTitle, item)[0]
            print(title)

        return title

    def get_page_content(self, soup):
        """获取单页文本内容"""
        content = "    "

        for item in soup.find_all('div',id="content"):
            item = str(item)
            text_list = re.findall(findText, item)
        
            for text in text_list:
                content = content + str(text) + '\n    '
        
        return content

    def writer(self, title, content):
        """向文本内写入内容"""
        with open(self.txt_path, 'a', encoding='utf-8') as f:  
            # 打开目标路径文件
            f.write(title + '\n')
            f.write(content)
            f.write('\n\n')
            print(f'wirte {title} success')
    
    def down(self, begin_url, end_url):
        cur_url = begin_url

        while(cur_url != end_url):
            
            soup = self.get_soup(cur_url)
            nextPageUrl = self.get_next_url(soup, 0)
            nextPageSoup = self.get_soup(nextPageUrl)

            title, content = None, ""

            title = self.get_title(soup)
            content += self.get_page_content(soup)
            content += self.get_page_content(nextPageSoup)
            
            self.writer(title, content)

            cur_url = self.get_next_url(nextPageSoup, 1)
        

if __name__ == "__main__":
    base_url = 'xxx'
    begin_url = 'xxx1'
    end_url = 'xxx2'

    txt_path = './1.txt'
    novel_down = downloader(base_url, txt_path)
    novel_down.down(begin_url, end_url)