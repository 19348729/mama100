from django.conf.urls import patterns, include, url
from django.contrib import admin
from mama100.cmdb.views import *
from mama100.cmdb.auto import *
from mama100.cmdb.manual import *
from mama100.cmdb.webssh import *
from mama100.cmdb.passwd import *
from mama100.cmdb.project import *
from mama100.cmdb.configremanager import *
from mama100.cmdb.records import *
from mama100.dockerweb.views import *
urlpatterns = patterns('',
    # Exampleswerer:
    # url(r'^$', 'mama100.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^index/$',index),
    url(r'^mannal/mannal_edit/$',mannal_edit),
    url(r'^mannal/mannal_edit/manualAdd$',manualAdd),
    url(r'^manual_index$',manual_index),
    url(r'^passwd$',hostpasswd_index),
###control
	url(r'^control$',control_index),


###login
    # url(r'^accounts/login/$',)
    url(r'^$',login_index),
    url(r'^login_check$',login_check),
    url(r'^login_check_only',login_check_only),
    url(r'^user_logout$',user_logout),
    url(r'^change_password/(?P<username>.*)$',change_password_index),
    url(r'^change_password_commit/$',change_password_commit),
###hostinfo
	url(r'^hostinfo_index$',hostinfo_index),
    url(r'^zyuser$',zyuser),

###passwd find
    url(r'^hostpasswd_find',hostpasswd_find),
    url(r'^hostpasswd_add',hostpasswd_add),
    url(r'^hostpasswd_auth',hostpasswd_auth),
    url(r'^batch_change_passwd',batch_change_passwd),

#####weebssh
    url(r'^webssh_index$',webssh_index),
    # url(r'^wssh/(?P<hostname>\d+\.\d+\.\d+\.\d+)/(?P<username>.*)$',webssh_connect),
    url(r'^wssh$',webssh_connect),
######project
    url(r'^project_info$',project_info),
    url(r'^project_edit/$',project_edit),
    url(r'^project_edit/project_edit_commit$',project_edit_commit),
    url(r'^project_create$',project_create),
    url(r'^project_create_commit$',project_create_commit),
    url(r'^project_delete$',project_delete),
    url(r'^project_online_build_job$',project_online_build_job),
######configure manager
    url(r'^networkdy_index$',networkdy_index),
    url(r'^config_edit$',config_edit),
    url(r'^get_file_info$',get_file_info),
    url(r'^config_info_commit$',config_info_commit),
######configure project cmdb
    url(r'^project_online$',project_online),
    url(r'^project_online_commit$',project_online_commit),

 #####docker managere

    url(r'^docker_images_index$',docker_images_index),
    url(r'^del_img',del_img),
    url(r'^docker_con_index',docker_con_index),
    url(r'^constopstart',constopstart),
    url(r'^docker_port',docker_port),
    url(r'^docker_maxport',docker_maxport),
 ########records ##############
    url(r'^records$',records),
 ########test ##############
    url(r'^form',form),
)


