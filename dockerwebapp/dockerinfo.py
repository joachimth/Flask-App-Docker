import docker
from cpuinfo import get_cpu_info
from psutil import virtual_memory

#Connect to Docker Socket
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
dockerinfo = client.version()

#Get CPU information
cpu = get_cpu_info()

#Get Memory Information
mem = virtual_memory()
ram = mem.total / 1024 / 1024 / 1024