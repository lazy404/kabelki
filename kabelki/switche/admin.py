from django.contrib import admin
from django import forms
from switche.models import *


class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'used_ports']
    #list_filter= ['backup_dir', 'rsync_source']
    #search_fields = ['rsync_source__server_name', 'rsync_source__ip']
    #list_editable=['backup_dir','active']
    save_on_top=True

admin.site.register(Host, HostAdmin)

class HostTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'used_ports']
    #list_filter= ['backup_dir', 'rsync_source']
    #search_fields = ['rsync_source__server_name', 'rsync_source__ip']
    #list_editable=['backup_dir','active']
    save_on_top=True

admin.site.register(HostType, HostTypeAdmin)


class PortAdmin(admin.ModelAdmin):
    list_display = ['name', 'port_type', 'speed']
    list_filter= ['port_type']
    #search_fields = ['rsync_source__server_name', 'rsync_source__ip']
    #list_editable=['backup_dir','active']
    save_on_top=True

admin.site.register(Port, PortAdmin)


class ConnectionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConnectionAdminForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        
        try:
            self.fields['porta'].queryset = self.instance.hosta.host_type.ports.all()
        except Exception as e:
            pass

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'hosta', 'porta', 'hostb', 'portb']
    list_filter= ['hosta', 'hostb']

    form=ConnectionAdminForm
    #search_fields = ['rsync_source__server_name', 'rsync_source__ip']
    #list_editable=['backup_dir','active']
    save_on_top=True

admin.site.register(Connection, ConnectionAdmin)
