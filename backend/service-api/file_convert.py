import cx_Oracle
import pandas as pd
import hashlib
import time
# 防止中文乱码
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# 根目录
base_dir = 'D:/项目文档/平高/SCM/convert_file'


# 连接Oracle数据库，执行操作
class Oracle(object):
    def __init__(self, user_name, password, host, prot, service_name):
        print("-------------创建数据库链接-------------")
        # 设置Oracle数据源名称
        dsn = cx_Oracle.makedsn(host, prot, service_name=service_name)
        # 创建数据库连接
        self.connect = cx_Oracle.connect(user=user_name, password=password, dsn=dsn)
        # 创建游标
        self.cursor = self.connect.cursor()

    def select(self, sql):
        """ 查询数据 """
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def disconnect(self):
        """ 关闭游标和连接 """
        self.cursor.close()
        self.connect.close()

    def insert(self, sql, list_param):
        try:
            self.cursor.executemany(sql, list_param)
            self.connect.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


def mkdir(path, file_name):
    """ 创建目录 """
    path = str(path).strip()  # 去除首尾空格
    path = str(path).rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)  # 不存在则创建目录

    return os.path.join(path, file_name)


if __name__ == '__main__':
    # 连接数据库参数
    oraDb = Oracle('PGSCM', 'qwertyuiop#789', '39.101.134.26', '1521', 'ORCL')
    # 查询系统附件表
    sql = "SELECT * FROM XTFJ ORDER BY CJSJ ASC"
    # 执行SQL
    data = oraDb.select(sql)
    not_list = []
    convert_list = []
    # 遍历并转换文件
    for index,row in enumerate(data):
        if row[11]:
            file_path = os.path.join(base_dir, row[2])
            # 文件名称
            if not row[2]:
                file_name = "{}.{}".format(row[0], row[6])
            else:
                file_name = "{}_{}.{}".format(row[2], int(time.time() * 1000), row[6])
            # 保存到数据库的文件路径
            save_file_path = os.path.join(row[2], file_name)
            # 输出文件路径
            out_file_path = mkdir(file_path, file_name)
            # 以二进制方式写文件
            file = open(out_file_path, 'wb')
            file.write(row[11].read())
            # 二进制MD5
            old_md5 = hashlib.md5(row[11].read()).hexdigest()
            # 以二进制形式读取生成的文件，用于比对文件完整性
            with open(out_file_path, 'rb') as file:
                file_content = file.read()
                new_md5 = hashlib.md5(file_content).hexdigest()

            convert_item = {
                "编号": row[0],
                "主键编号": row[1],
                "二进制MD5": old_md5,
                "文件MD5": new_md5,
                "结果": old_md5 == new_md5
            }
            convert_list.append(convert_item)
            print("第【{}】条，编号：【{}】，文件类型：【{}】，保存路径：【{}】，文件完整性：【{}】".format(index + 1,row[0], row[2], save_file_path, old_md5 == new_md5))
        else:
            not_item = {
                "编号": row[0],
                "主键编号": row[1],
                "附件类型": row[2],
                "创建时间": row[9],
                "创建人": row[10]
            }
            not_list.append(not_item)
            print("第【{}】条数据，编号【{}】的数据无文件内容！".format(index + 1, row[0]))

    convert_df = pd.DataFrame(convert_list)
    convert_file_path = os.path.join(base_dir, "convert_file.csv")
    convert_df.to_csv(convert_file_path, encoding="GBK", index=False)

    not_df = pd.DataFrame(not_list)
    not_file_path = os.path.join(base_dir, "not_convert.csv")
    not_df.to_csv(not_file_path, encoding="GBK", index=False)
    # 断开数据库连接
    oraDb.disconnect()
    print("-------------文件转换完成-------------")