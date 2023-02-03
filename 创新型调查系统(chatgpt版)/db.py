import sqlite3

# 2、创建数据表
conn = sqlite3.connect("collect_data.db")  # 打开或创建数据库
print("成功打开数据库")

c = conn.cursor()  # 获取游标
sql = '''
    create table company
        (ID INTEGER PRIMARY KEY,
        Users char[300] not null,
        ChatGPT char[300] not null);
    '''
c.execute(sql)  # 执行SQL语句
conn.commit()  # 提交数据库操作
conn.close()  # 关闭数据库链接


print("成功建表")