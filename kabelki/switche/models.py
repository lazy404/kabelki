#
# encoding: utf-8

from django.db import models
from smart_selects.db_fields import ChainedForeignKey 

PORT_TYPE = (
    ('ethernet', 'ethernet'),
    ('kvm', 'KVM'),
)

class Port(models.Model):
    class Meta:
        verbose_name_plural='Porty'
        verbose_name='Port'
    name=models.CharField(max_length=256, blank=False)
    port_type=models.CharField(max_length=16, choices=PORT_TYPE, editable=True, default='eth')
    speed=models.IntegerField(help_text='Port speed', default=1000)
    comment = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return u'%s (%s)' %(self.port_type, self.name)

class HostType(models.Model):
    class Meta:
        verbose_name_plural='Typy Hostów'
        verbose_name='Typ hosta'
    name=models.CharField(max_length=256, blank=False)
    comment=models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name

class Host(models.Model):
    class Meta:
        verbose_name_plural='Hosty'
        verbose_name='Host'
    name=models.CharField(max_length=256, blank=False)
    host_type=models.ForeignKey(HostType, blank=False)
    ports=models.ManyToManyField(Port)
    
    active=models.BooleanField(default=True)
    comment=models.CharField(max_length=256, blank=True)

    def used_ports(self):
        return ", ".join([p.name for p in self.ports.all()])

    def __unicode__(self):
        return u'%s - %s' %(self.host_type.name, self.name)

class Connection(models.Model):
    class Meta:
        verbose_name_plural='Połączeniay'
        verbose_name='Połączenie'
        unique_together=(('hosta','porta','hostb','portb'))
        
    name=models.CharField(max_length=256, blank=False)
    hosta=models.ForeignKey(Host, blank=False)

    porta = ChainedForeignKey(
            Port, 
            chained_field="hosta",
            chained_model_field="name", 
            show_all=False, 
            auto_choose=True)

    porta=models.ForeignKey(Port, blank=False)
    hostb=models.ForeignKey(Host, blank=False, related_name='hostb_link')
    portb=models.ForeignKey(Port, blank=False, related_name='portb_link')
    active=models.BooleanField(default=True)
    comment=models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return u'%s(%s) - %s(%s)' %(self.hosta.name, self.porta.name, self.hostb.name, self.portb.name)

t='''
    interval=models.IntegerField(help_text='Co jaki czas wykonywac backup, np. to co 2 dni', default=2)
    offset=models.IntegerField(help_text='Przesuniecie interval wzgledem poczatku roku', default=0)
    max_level=models.IntegerField(help_text='Max ilosc przyrostow', default=2)
    level=models.IntegerField(help_text='Aktualny przyrost', default=0, editable=False)
    prio=models.IntegerField(help_text='Priorytet, im wiekszy tym backup bedzie wykonany wczesniej', default=0)
    comment = models.CharField(max_length=256, blank=True)
    
    def __unicode__(self):
        return u'%s - %s' %(self.rsync_source,self.backup_dir)

    def lastBackup(self):
        lg=JobQueue.objects.filter(Q(backup_job=BackupJob.objects.get(pk=self.pk)) & Q(status='DONE')).order_by('-start')
        
        if len(lg) > 0:
            return str(lg[0].end)
        else:
            return ""
'''