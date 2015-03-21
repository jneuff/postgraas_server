__author__ = 'sebastian neubauer'
import docker
import hashlib


def get_unique_id(connection_dict):
    return hashlib.sha1(str(frozenset(connection_dict.items()))).hexdigest()


def get_hostname():
    return "weather-test1"


def get_open_port():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port


def create_postgres_instance(connection_dict):
    #docker run -d -p 5432:5432 -e POSTGRESQL_USER=test -e POSTGRESQL_PASS=oe9jaacZLbR9pN -e POSTGRESQL_DB=test orchardup/postgresql
    c = docker.Client(base_url='unix://var/run/docker.sock',
                  timeout=30)
    environment = {
        "POSTGRES_USER": connection_dict['db_username'],
        "POSTGRES_PASS": connection_dict['db_pwd'],
        "POSTGRES_DB": connection_dict['db_name']
    }
    internal_port = 5432
    container_info = c.create_container('postgres', ports=[internal_port], environment=environment)
    container_id = container_info['Id']
    port_dict = {internal_port: connection_dict['port']}
    c.start(container_id, port_bindings=port_dict)
    return container_id


def delete_postgres_instance(container_id):
    c = docker.Client(base_url='unix://var/run/docker.sock',
                  timeout=30)
    print c.remove_container(container_id, force=True)
    return True