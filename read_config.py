from datasource import Datasource


class ReadConfig(object):
    def __init__(self):
        pass


class ReadDatabaseConfig(ReadConfig):
    def __init__(self, source: Datasource, job_id):
        ReadConfig.__init__(self)
        self.source = source
        self.job_id = job_id
        self.job = self.__job()
        self.user = self.__user()
        self.proxy = self.__proxy()

    def __job(self):
        return self.source.one('select * from job where id = \'' + str(self.job_id) + '\';')

    def __user(self):
        return self.source.one('select * from `user` where id = \'' + str(self.job['user_id']) + '\';')

    def __proxy(self):
        if self.job['use_proxy'] == 1:
            return self.source.one('select * from `proxy` where id = \'' + str(self.job['proxy_id']) + '\';')
        else:
            return None


class ReadJsonConfig(ReadConfig):
    def __init__(self, source):
        ReadConfig.__init__(self)
        self.job = source['job']
        self.user = source['user']
        self.proxy = source['proxy']
