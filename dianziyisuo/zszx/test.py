 # -*- coding: utf-8 -*- 
import pymysql
from bs4 import BeautifulSoup
import requests





html_doc = """
<p>面对如此层出不穷的网络诈骗手段，球迷们应该如何应对呢?卡巴斯基实验室的专家提供四点建议，助球迷们远离网络威胁，乐享足球狂欢季。<br/>1. 一定要在输入任何登录或机密信息之前仔细检查网页。<br/>2. 虽然以“https”开头的网站较之“http”更为安全，但这并不表示可以完全信任这些网站。网络罪犯能够通过其他渠道获得合法的SSL证书。<br/>3. 警惕不明发件人的邮件，尤其不要打开来源不明的邮件中的链接和附件，不要从不受信任的网站下载文件。<br/>4. 确保计算机上安装了反恶意软件产品，拦截钓鱼网站。</p><p>为了防范以世界杯话题为诱饵网络威胁，趋势科技建议用户采取以下措施进行防范：</p><p>1、下载世界杯相关应用、上网参与世界杯讨论等网络活动时，请尽量选择官方渠道，并谨慎辨别链接的安全性。</p><p>2、谨慎访问赌球、博彩等地下网站，这些网站往往是威胁传播的最好载体，而且监管措施相对薄弱，很容易导致用户被恶意软件或钓鱼网站入侵。</p><p>3、在讨论与世界杯相关话题时，保持头脑清醒，不要随意点击社交网站上发过来的陌生链接，也不要随意扫描相关二维码。</p><p>4、安装PC-cillin 2014云安全版等具有强大防恶意软件、防钓鱼网站的网络安全软件。</p><p><br/></p>
"""
soup = BeautifulSoup(html_doc, 'lxml')
new_content = soup.get_text()
# for para in soup.find_all():
# 	new_content += para.get_text()
# new_content = new_content.replace("'", "\\'")
# new_content = new_content.replace('"', '\\"')
# elif soup.find('table'):
# 	for para in soup.find_all('table'):
# 		new_content += para.get_text()
# 		new_content = new_content.replace("'", "\\'")
# 		new_content = new_content.replace('"', '\\"')
# else:
# 	for para in soup.find_all('p'):
# 		new_content += para.get_text()
# 		new_content = new_content.replace("'", "\\'")
# 		new_content = new_content.replace('"', '\\"')
		
print(new_content)


