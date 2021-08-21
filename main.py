from dcconfig import BaseService, Compose

class BaseDb(BaseService):
    def __init__(self, name):
        super(BaseDb, self).__init__(name)

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

class BaseApiService(BaseService):
    def __init__(self, name):
        super(BaseApiService, self).__init__(name)

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

class Nginx(BaseService):
    def __init__(self):
        super(Nginx, self).__init__()

        self.depends_on = ['apiservice', 'api_empty', 'admin']
        self.build = './nginx'
        self.ports = ['80:80', '443:443']
        self.volumes = ['./nginx/nginx.conf:/etc/nginx/nginx.conf', './nginx/cert:/cert']
        self.environment = {
            'TZ' : 'Asia/Shanghai'
        }

class Redis(BaseService):
    def __init__(self):
        super(Redis, self).__init__()

        self.image = 'redis:6'
        self.command = 'redis-server --requirepass passwd'
        self.ports = ['6379:6379']

db = BaseDb('db')
empty_classroom_db = BaseDb('empty_classroom_db')
nginx = Nginx()
redis = Redis()
services = [db, empty_classroom_db, nginx, redis]

my_compose = Compose()
my_compose.add_services(services)

my_compose.build_file('./test.yml')

