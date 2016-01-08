#coding=utf-8
#!/usr/bin/env python
# __author__ = 'liming'
'''
    获取所有的DOCERK的主机CPU、内存信息
'''

from mysql_run import *
from zabbix.sum_result import *
from ssh_run import *
import docker
###从数据库的cmdb_auto_info表取出所有的DOCKER主机
def get_docker_ip():
    sql='select ip from cmdb_auto_info where has_process like "docker"'
    a=conn_mysql(sql)
    ip_list=[]
    for i in a:
       ip_list.append(i[0])
    return ip_list

###取分IP地址，分为生产和测试两部分
def list_to_dict(list_a):
    ip_dict={}
    ip_dict['prd']=[]
    ip_dict['test']=[]
    for i in list_a:
        if '192.168.115' in i:
            ip_dict['test'].append(i)
        else:
            ip_dict['prd'].append(i)
    return ip_dict



##取生产环境或是测试环境下对应IP的内存和CPU的使可用值
def get_dict_value(type='prd'):
    dict_sum_cpu={}
    dict_sum_mem={}
    dict_sum={}

    ip_list=get_docker_ip()###所有DOCKER的IP
    b= list_to_dict(ip_list)####变换成字典，分类成生产和测试两个KEY
    for i in b[type]:
        dict_sum_mem[i]=get_result(i,1)['memoryfree']['value'][0]
        dict_sum_cpu[i]=get_result(i,1)['cpu']['value'][0]

######cpu按正序排列，内存为倒序排列，最后组合成一个字典
    dict_sum['cpu']=sorted(dict_sum_cpu.items(), key=lambda d: d[1])
    dict_sum['mem']=sorted(dict_sum_mem.items(), key=lambda d: d[1], reverse=True)
    return dict_sum
# print get_dict_value()

#####给定需要的主机数量，取出内存最空闲的机器IP,此函数没有考虑CPU的性能指标
def get_host(host_numbers,type='prd'):
    host_list=[]
    dict_sum=get_dict_value(type)
    dict_len=len(dict_sum['mem'])

#####如果只有四个主机你又要6个节点，我只能说 to more 了
    if int(host_numbers) <= int(dict_len):
    # for i in range(host_numbers):
        for i in dict_sum['mem'][0:int(host_numbers)]:
            host_list.append(i[0])
        return host_list
    else:
        return 'to more'

#####由IP列表，软件类型，软件名称，端口来创建容器
def docker_create(ip_list,env,soft_type,soft_name,port_dict,build_path):
    dir_name='/opt/applications/'+env+'_'+soft_name
    print "my ip is ;%s" %ip_list
    print port_dict
    ip_temp=['192.168.234.175']
    for i in ip_list:
        print type(i)
        print type(port_dict)
        port=port_dict[i]
        password=get_password(i)
        del_yes(i)
        cmd1='mkdir -p '+ dir_name
        run_ssh(i,'root',password,cmd1)
        c=docker.Client(base_url='tcp://'+i+':2375',version='1.17',timeout=10)
        if 'rpc' in soft_type:
            img_name='rpc_mode'####镜像模板名为rpc
            cmd2='cp /opt/applications/rpc/run.sh '+dir_name ###复制通用的RPC启动脚本
            run_ssh(i,'root',password,cmd2)
            dir_bind=[''+dir_name+':'+'/mnt/']

            #commd_file='scp -r 192.168.234.17:'+build_path+'*.jar '+dir_name
           # print commd_file
            #run_ssh(i,'root',password,commd_file)
######针对GLASSFISH的应用暂时不启用
        # else:
        #     img_name='glassfish4_mode'####镜像模板名为glassfish
        #     cmd2='cp /opt/applications/glassfish/run.sh /opt/applications/'+env+'_'+soft_name
        #     app_log='/opt/logs/'+env+'_'+soft_name
        #     cmd3='mkdir -p '+ app_log
        #     run_ssh(i,'root',password,cmd2)
        #     run_ssh(i,'root',password,cmd3)
        #     log_dir="/opt/glassfish/glassfish/domains/domain1/logs"
        #     app_dir="/opt/webapp/"+soft_name
        #     dir_bind=[''+dir_name+':'+app_dir+'',''+app_log+':'+log_dir+'']
        #     print "log dir is %s" %dir_bind

            # port_dict={8080:int(max_port)+1,4848:int(max_port)+2}
            # print "log port is %s" %port_dict
            # commd_file='cp -r '+build_path+'*.war '+dir_name
            # print commd_file
            # print run_ssh(i,'root',password,'ls '+build_path)
            # print run_ssh(i,'root',password,commd_file)
        # if port_dict:###glassfish
        #     container=c.create_container(image=img_name,name=env+'_'+soft_name,ports=[8080,4848],command=app_dir+'/run.sh '+soft_name,host_config=docker.utils.create_host_config(binds=dir_bind,port_bindings=port_dict))
        # else:##rpc
        container=c.create_container(image=img_name,name=env+'_'+soft_name,command='/mnt/run.sh '+i+' '+str(int(port)+1),host_config=docker.utils.create_host_config(binds=dir_bind,network_mode='host'))
        #c.start(container=container.get('Id'))


if __name__=='__main__':
    print get_host(6)
