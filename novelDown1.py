"""
python 爬虫系列，下载小说保存为 txt
"""
import re
import requests
from bs4 import BeautifulSoup

# 根据不同的网页，写不同的正则表达式匹配
findChap = re.compile(r'<a class="chapter-li-a" data-chapter-id="(.*?)" href="(.*?)">')
findLink = re.compile(r'\'(.*?)\'')
findTitle = re.compile(r'<h3>(.*?)</h3>',re.S)
findText = re.compile(r'<p>(.*?)</p>',re.S)

class downloader(object):

    def __init__(self, base_url, txt_path):
        self.base_url = base_url  
        self.txt_path = txt_path  

    def get_soup(self, url):
        headers = { 'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/15.1 Safari/605.1.15'}

        req = requests.get(url = url, headers=headers)
        req.encoding = req.apparent_encoding
        soup = BeautifulSoup(req.text, 'html.parser')

        return soup

    def get_chap_url(self, logurl):
        soup = self.get_soup(logurl)
        self.chap_url = []

        for item in soup.find_all('li',class_="chapter-li jsChapter"):
            item = str(item)
            # print(item)
            link_temp = str(re.findall(findChap, item)[0])
            link = re.findall(findLink, link_temp)[1]
            
            url = self.base_url + str(link)

            if url == 'https://m.aaread.club/book/1962/184576' \
                or url == 'https://m.aaread.club/book/1962/184577' \
                or url == 'https://m.aaread.club/book/1962/126875' \
                or url == 'https://m.aaread.club/book/1962/126876':
                continue

            self.chap_url.append(url)

        print(len(self.chap_url))

    def get_chap_content(self, soup):
        """获取单章文本标题以及内容"""
        content = ""
        
        for item in soup.find_all('article', id="chapterContent"):
            item = str(item)

            title = re.findall(findTitle, item)[0]

            text_list = re.findall(findText, item)
        
            for text in text_list:
                content = content + str(text) + '\n'
        
        return title, content

    def writer(self, title, content):
        """向文本内写入内容"""
        with open(self.txt_path, 'a', encoding='utf-8') as f:  
            # 打开目标路径文件
            f.write(title + '\n')
            f.write(content)
            f.write('\n\n')
            print(f'wirte {title} success')
    
    def down(self):
        
        for url in self.chap_url:
            
            soup = self.get_soup(url)
            title, content = self.get_chap_content(soup)
            self.writer(title, content)
        

if __name__ == "__main__":
    base_url = ''

    txt_path = './1.txt'
    novel_down = downloader(base_url, txt_path)
    novel_down.get_chap_url('')
    novel_down.down()