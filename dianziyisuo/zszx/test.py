 # -*- coding: utf-8 -*- 
import pymysql
from bs4 import BeautifulSoup

html_doc = """
 <abstract><![CDATA[本发明公开了一种Ag<sub>2<sub>Ga纳米针成型机理及尖端形貌控制研究方法按如下步骤一、计算模型建立Ag微粒与Ga微粒发生化学反应生成Ag<sub>2sub>Ga用方程2Ag+GaAg<sub>2<sub>Ga表示在整个计算模型中存在着三个密度场变量定义Ag微粒为c<sub>1<sub>(x,y,z,t)Ag<sub>2sub>Ga纳米针为c<sub>2sub>(x,y,z,t)Ga微粒为c<sub>3<sub>(x,y,z,t)c<sub>1<sub>为Ag微粒的浓度占总的微粒浓度的百分比c<sub>2sub>为Ag<sub>2sub>Ga微粒的浓度占总的微粒浓度的百分比c<sub>3<sub>为Ga微粒的浓度占总的微粒浓度的百分比该计算模型自由能主要由化学能和梯度能组成用如下方程表示<maths num="0001"><math><![CDATA[ <mrow> <mi>G<mi> <mo>=<mo> <munder> <mo>&Integral;mo> <mi>vmi> munder> <mo>{mo> <msub> <mi>Fmi> <mrow> <mi>cmi> <mi>hmi> mrow> m<sub> <mo>+mo> <msub> <mi>Fmi> <mrow> <mi>gmi> <mi>rmi> <mi>ami> <mi>dmi> mrow> msub> <mo>}mo> <mi>d<mi> <mi>V<mi> <mo>-mo> <mo>-mo> <mo>-mo> <mrow> <mo>(mo> <mn>1mn> <mo>)mo> mrow> mrow>]]></math><img file="DDA0001000527100000011.TIF" wi="510" he="111" /></maths>其中F<sub>ch<sub>表示化学能量变化F<sub>grad<sub>表示梯度能量变化二、通过改变材料的表面能来探究纳米针尖端形貌变化的作用规律控制不同材料纳米针尖端形貌变化。]]></abstract>

"""
soup = BeautifulSoup(html_doc)
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
print("dddd")


