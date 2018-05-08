# -*- coding: UTF-8 -*-
import random

from util.sql_db_helper import DBHelper


def get_sql_cpname(params=None):
    """
    @summary:执行查询库中公司名名单，并取出所有结果集
    @params可选参数，条件list值（元组/列表）,['limit:n','tabNum:n','random:Y'],每张表获取名单数量，多少张表中获取
    @return:result list/boolean 返回数据库中公司名单
    """
    tables = []
    access_table = []
    for x in range(100):
        tables.append('%s%s' % ('CompanyDiretory_', str(x), ))
    tables_num = 5
    if params is None:
        limit_condition = ' limit 2'
    else:
        for p in params:
            p_key = p.split(':')[0]
            p_value = p.split(':')[1]
            if 'limit'.__eq__(p_key):
                limit_condition = '%s%s%s' % (p_key, ' ', p_value)
            elif 'tabNum'.__eq__(p_key):
                tables_num = int(p_value)
            elif 'random'.__eq__(p_key):
                random.shuffle(tables)
    db = DBHelper()
    companys_list = []
    i = 0
    for table in tables:
        if i >= tables_num:
            break
        i = i + 1
        print(table)
        companys_table_list = db.query_all("select CompanyName from " + table + " order by rand() " + limit_condition, )
        companys_list.extend(companys_table_list)
    db.release()
    return companys_list

if __name__ == '__main__':
    get_sql_cpname(['limit:5', 'tabNum:2', 'random:Y'])
