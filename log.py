from read_config import ReadDatabaseConfig
import pymysql
import datetime


class Log(object):
    def __init__(self):
        pass


class DatasourceLog(Log):
    def __init__(self, read: ReadDatabaseConfig, exec_id: str):
        self.exec_id = exec_id
        self.read = read

    def info(self, content: str):
        self.read.source.insert('insert into job_log (job_exec_id, create_time, type, content)' +
                                'values (' + str(self.exec_id) + ', sysdate(), \'info\', \'' + pymysql.escape_string(content) + '\')')

    def error(self, content: str):
        self.read.source.insert('insert into job_log (job_exec_id, create_time, type, content)' +
                                'values (' + str(self.exec_id) + ', sysdate(), \'error\', \'' + pymysql.escape_string(content) + '\')')


class LocalLog(Log):
    def __init__(self, log: str):
        self.log = log

    def info(self, content: str):
        f = open(self.log, 'a')
        out = '[' + str(datetime.datetime.now()) + '] : [info] : ' + content + '\n'
        f.write(out)
        f.close()

    def error(self, content: str):
        f = open(self.log, 'a')
        out = '[' + str(datetime.datetime.now()) + '] : [error] : ' + content + '\n'
        f.write(out)
        f.close()
