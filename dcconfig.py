from ruamel import yaml

class BaseService():
    def __init__(self, name=None):
        if name == None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def __str__(self):
        return f'{self.__class__.__name__} object (name: {self.name})'

    def get_dict(self):
        dict = self.__dict__.copy()
        del dict['name']
        return dict
        

class Compose():
    def __init__(self, version=3):
        self.version = 3
        self.servers = []
    
    def add_service(self, service):
        self.servers.append(service)

    def add_services(self, services):
        self.servers.extend(services)

    def build_dict(self):
        data = {}
        data['version'] = f'{self.version}'
        data['services'] = {}
        for service in self.servers:
            data['services'][service.name] = service.get_dict()
        return data

    def build_file(self, filename):
        data = self.build_dict()
        with open(filename, 'w') as distFile:
            yaml.dump(data, distFile, Dumper=yaml.RoundTripDumper)

