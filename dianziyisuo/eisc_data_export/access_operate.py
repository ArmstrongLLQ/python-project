# -*- coding: utf-8 -*-
'''
python 操作 access数据库
'''
import pypyodbc

#建立数据库连接
def mdb_conn(db_name, password = ""):
    """
    功能：创建数据库连接
    :param db_name: 数据库名称
    :param db_name: 数据库密码，默认为空
    :return: 返回数据库连接
    """
    str = 'Driver={Microsoft Access Driver (DE2014001.mdb)};PWD' + password + ";DBQ=" + db_name
    conn = pypyodbc.connect(str)
    cursor = conn.cursor()
    return conn, cursor

#查询记录
def mdb_sel(cur, sql):
    """
    功能：向数据库查询数据
    :param cur: 游标
    :param sql: sql语句
    :return: 查询结果集
    """
    try:
        cur.execute(sql)
        return cur.fetchall()
    except:
        return []

def main():
    mdb_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\要更改的能源报告数据表\\DE2014001.mdb'
    table_name = 'Data'
    conn, cursor = mdb_conn(mdb_file)

    sql = 'select id from ' + table_name + 'where id < 10'

    data = mdb_sel(cursor, sql)

    print(data)

    cursor.close()
    conn.close()

# 光盘号,会议录名称,英文会议录名称,ISSN,CN,ISBN,年,卷,期刊基本参数,期,文件名,论文题名,论文作者,
# 作者机构,文章编号,文章属性,语种,分类号,论文摘要,论文关键词,收稿日期,基金,作者简介,英文论文题名,
# 英文论文作者,英文论文摘要,英文论文关键词,引文,期刊页码,物理页码,学会代码,代码,ZJ,COLCODE,ZJCOL,
# 专题代码,子栏目代码,专题子栏目代码,全文,发行范围,会议名称,英文会议名称,会议地点,主办单位,编者,
# 出版单位,出版日期,学会名称,专委会名称,编辑部名称,主编,内部资料否,全文否,更新日期,中英文题名,
# 复合关键词,中英文摘要,主题,旧机标关键词,OLD_SYS_VSM,来源数据库,页数,文件大小,第一责任人,中英文会议名称,
# 中英文会议录名称,DOI,专辑代码,正文快照,中英文作者,网络出版投稿时间,网络出版投稿人,原文格式,下载频次,
# 被引频次,文献标识码,文献类型标识,来源标识码,主题词,KMC分类号,语义树条码,发表时间,基金代码,作者代码,
# 机构代码,TABLENAME	表名,是否含新概念,所含新概念名称,新概念代码,概念出处,是否高下载,是否高被引,是否高他引,
# 他引频次,是否基金文献,机构作者代码,报告级别,报告级别代码,会议级别,会议级别代码,会议召开时间,栏目层次,主办单位代码,
# 论文集类型,文献作者,来源代码,FFD	SMARTS,机标关键词,SYS_VSM,出版物代码

if __name__ == '__main__':
    main()