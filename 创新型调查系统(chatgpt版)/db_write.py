import sqlite3

# 3、插入数据
conn = sqlite3.connect("test.db")  # 打开或创建数据文件
print("成功打开数据库")

c = conn.cursor()  # 获取游标
sql1 = '''
    insert into company(id,name,age,address,salary)
    values(1,'张三',32,"北京",18000);
'''
sql2 = '''
    insert into company(id,name,age,address,salary)
    values(2,'李四',29,"武汉",15000);
'''

c.execute(sql1)  # 执行SQL语句
c.execute(sql2)  # 执行SQL语句
conn.commit()  # 提交数据库操作
conn.close()  # 关闭数据库链接

print("插入数据完毕")