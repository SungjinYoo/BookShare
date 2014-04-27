# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'users_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('last_login_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'users', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'users_user')


    models = {
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_login_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['users']