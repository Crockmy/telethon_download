import pymysql


class Datasource:
    def __init__(self,
                 host,
                 port,
                 user,
                 password,
                 db,
                 charset
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def connect(self):
        # 连接数据库
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset=self.charset
        )

    def __dict_cursor(self, conn):
        return conn.cursor(cursor=pymysql.cursors.DictCursor)

    def one(self, sql: str):
        _conn = self.connect()
        _cursor = self.__dict_cursor(_conn)
        _rows = _cursor.execute(sql)
        if _rows != 1:
            raise Exception("返回结果!=1, sql:" + sql)
        _result = _cursor.fetchone()
        _cursor.close()
        _conn.close()
        return _result

    def list(self, sql: str):
        _conn = self.connect()
        _cursor = self.__dict_cursor(_conn)
        _cursor.execute(sql)
        _result = _cursor.fetchAll()
        _cursor.close()
        _conn.close()
        return _result

    def insert(self, sql: str):
        _conn = self.connect()
        _cursor = self.__dict_cursor(_conn)
        _cursor.execute(sql)
        _result = _conn.insert_id()
        _conn.commit()
        _cursor.close()
        _conn.close()
        return _result

    def update(self, sql: str):
        _conn = self.connect()
        _cursor = self.__dict_cursor(_conn)
        _result = _cursor.execute(sql)
        _conn.commit()
        _cursor.close()
        _conn.close()
        return _result
