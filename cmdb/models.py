# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#####自动发现抓取回服务器基本信息表
class cmdb_auto_info(models.Model):
    ip=models.CharField(max_length=100)
    cpu=models.CharField(max_length=50)
    disk=models.CharField(max_length=50)
    mem=models.CharField(max_length=50)
    ip_list=models.CharField(max_length=500)
    has_process=models.CharField(max_length=50)
    vorw=models.CharField(max_length=50,null=True)
    parent_ip=models.CharField(max_length=50,null=True)
    os_type=models.CharField(max_length=150)
    mac=models.CharField(max_length=500)###MAC
    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)

    class Meta:
        db_table = 'cmdb_auto_info'
    def __unicode__(self):
         return ip
####对物理主机的基本信息手工添加表
class cmdb_manual_info(models.Model):
    ip=models.CharField(max_length=100)
    online_time=models.DateTimeField(auto_now=False,null=True)
    u_size=models.CharField(max_length=50,null=True)
    brand=models.CharField(max_length=500,null=True)  ##品牌
    jigui_number=models.CharField(max_length=50,null=True)

    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)

    class Meta:
        db_table = 'cmdb_manual_info'
    def __unicode__(self):
        return ip


class cmdb_process_info (models.Model):
    ip=models.CharField(max_length=100)
    nodes=models.CharField(max_length=50)
    project=models.CharField(max_length=50)
    config_file=models.CharField(max_length=50)
    restart_command=models.CharField(max_length=200)

    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)

    class Meta:
        db_table = 'cmdb_process_info'
    def __unicode__(self):
        return ip

class cmdb_operation_info (models.Model):
    ip=models.CharField(max_length=100)
    recode_info=models.CharField(max_length=50)#操作记录
    operation_time=models.DateTimeField()   ##操作时间
    operation_man=models.CharField(max_length=50)#操作人
    operation_style=models.CharField(max_length=50)#操作等级
    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)
    class Meta:
        db_table = 'cmdb_operation_info'
    def __unicode__(self):
        return ip

class cmdb_jigui_info(models.Model):
    number=models.CharField(max_length=50)
    dianya=models.CharField(max_length=50)
    user_pace=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)
    class Meta:
        db_table = 'cmdb_jigui_info'
    def __unicode__(self):
        return number


class cmdb_connect_info(models.Model):
    brand=models.CharField(max_length=50)
    connect_name=models.CharField(max_length=50)
    connect_tel=models.CharField(max_length=50)
    prod_type=models.CharField(max_length=50)
    other1=models.CharField(max_length=200,null=True)
    other2=models.CharField(max_length=200,null=True)
    class Meta:
        db_table = 'cmdb_connect_info'
    def __unicode__(self):
        return brand

####所有服务器密码管理表
class hostpasswd(models.Model):
        ip=models.CharField(max_length=50)
        username=models.CharField(max_length=50)
        password=models.CharField(max_length=500)
        password_temp=models.CharField(max_length=500)
        other1=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'hostpasswd'
        def __unicode__(self):
                return self.ip

####项目展示用表格
class cmdb_project(models.Model):
        jg_name=models.CharField(max_length=500) ## 架构名称
        project_name=models.CharField(max_length=500)## 项目名称
        online_time=models.DateTimeField()
        kaifa_man=models.CharField(max_length=100)
        soft_name=models.CharField(max_length=500,null=True)
        soft_type=models.CharField(max_length=500,null=True)
        nodeip=models.CharField(max_length=500,null=True)
        ent_type=models.CharField(max_length=500,null=True)## 1 生产 2 测试 3 开发
        other1=models.CharField(max_length=200,null=True)
        other2=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'cmdb_project'
        def __unicode__(self):
                return self.project_name
#######项目名与服务器IP对应表
class cmdb_project_auto(models.Model):
        project=models.CharField(max_length=500)
        ip=models.CharField(max_length=100)
        other2=models.CharField(max_length=500,null=True)
        other1=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'cmdb_project_auto'
        def __unicode__(self):
                return self.project

#######内外网对应关系表
class cmdb_networkdy(models.Model):
        nip=models.CharField(max_length=500)
        wip=models.CharField(max_length=500)
        other2=models.CharField(max_length=500,null=True)
        other1=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'cmdb_networkdy'
        def __unicode__(self):
                return self.nip


#####项目基础表，级关系
class cmdb_project_base(models.Model):
        project_name=models.CharField(max_length=500)
        project_father=models.CharField(max_length=500)
        other1=models.CharField(max_length=200,null=True)
        other2=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'cmdb_project_base'
        def __unicode__(self):
                return self.project_name

#####操作记录表
class cmdb_operation_records(models.Model):
        type=models.CharField(max_length=100)
        records=models.CharField(max_length=1000)
        project=models.CharField(max_length=200,null=True)
        operation_name=models.CharField(max_length=200,null=True)
        time=models.CharField(max_length=200,null=True)
        type_level=models.CharField(max_length=100)
        other1=models.CharField(max_length=500,null=True)
        other2=models.CharField(max_length=200,null=True)
        class Meta:
                db_table = 'cmdb_operation_records'
        def __unicode__(self):
                return self.project_name