from ruamel import yaml
import argparse

class baseService():
    def __init__(self, name):
        self.name = name
    
    def getDict(self):
        dict = self.__dict__
        del dict['name']
        return dict

class baseDb(baseService):
    def __init__(self, name):
        super().__init__(name)

        self.image = 'postgres:13'
        self.restart = 'always'
        self.environment = {
            'POSTGRES_USER': 'postgres',
            'POSTGRES_PASSWORD' : 'passwd',
            'POSTGRES_DB' : 'gostudy',
            'TZ' : 'Asia/Shanghai' 
        }
        self.ports = ['5678:5432']
        self.volumes = ['./data/postgres-data:/var/lib/postgresql/data']

class baseApiService(baseService):
    def __init__(self, name):
        super().__init__(name)

        self.build = './apiservice'
        self.volumes = ['./apiservice:/usr/src/app']
        self.depends_on = ['db']
        self.ports = ['1234:1234']
        self.enviroment = {
            'DEBUG': '\'FALSE\'',
            'TZ': 'Asia/Shanghai',
            'GIN_MODE': 'release',
            'TEST_INSERT': '\'TRUE\'',
            'TEST_REINIT': '\'TRUE\'',
            'ISSUER': 'apiserver',
            'SECRET': 'ExampleSecret',
            'APPID': 'ExampleAppID',
            'APPSECRET': 'ExampleAppSecret',
            'ADMIN_ID': 'ExampleADMIN_ID',
            'ADMIN_PASSWD': 'ExampleADMIN_PASSWD',
            'TEST_WX': '\'FALSE\''
        }

class nginx(baseService):
    def __init__(self):
        super().__init__('nginx')

        self.depends_on = ['apiservice', 'api_empty', 'admin']
        self.build = './nginx'
        self.ports = ['80:80', '443:443']
        self.volumes = ['./nginx/nginx.conf:/etc/nginx/nginx.conf', './nginx/cert:/cert']
        self.environment = {
            'TZ' : 'Asia/Shanghai'
        }

class redis(baseService):
    def __init__(self):
        super().__init__('redis')

        self.image = 'redis:6'
        self.command = 'redis-server --requirepass passwd'
        self.ports = ['6379:6379']
        

class Config():
    def __init__(self, version=3):
        self.version = 3
        self.servers = {}
    
    def addDb(self, name):
        self.servers[name] = baseDb(name)
    
    def addApiService(self, name):
        self.servers[name] = baseApiService(name)

    def addNginx(self):
        self.servers['nginx'] = nginx()

    def addRedis(self):
        self.servers['redis'] = redis()

    def buildConfigDict(self):
        data = {}
        data['version'] = f'{self.version}'
        data['services'] = {}
        for serviceName, serviceClass in self.servers.items():
            data['services'][serviceName] = serviceClass.getDict()
        return data

    def buildConfigFile(self, filename):
        data = self.buildConfigDict()
        with open(filename, 'w') as distFile:
            yaml.dump(data, distFile, Dumper=yaml.RoundTripDumper)
        print(data)

# usage:
# c = Config()
# c.addDb('db')
# c.addDb('empty_classroom_db')
# c.addApiService('apiservice')
# c.addApiService('api_empty')
# c.addNginx()
# c.addRedis()
# c.buildConfigFile('./docker-compose.yml')
