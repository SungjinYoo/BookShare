# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BookInstance'
        db.delete_table(u'books_bookinstance')


    def backwards(self, orm):
        # Adding model 'BookInstance'
        db.create_table(u'books_bookinstance', (
            ('status', self.gf('django.db.models.fields.CharField')(default='available', max_length=10)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('imported_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
        ))
        db.send_create_signal(u'books', ['BookInstance'])


    models = {
        u'books.book': {
            'Meta': {'object_name': 'Book'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['books.Course']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'books.course': {
            'Meta': {'object_name': 'Course'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'default': "u'spring'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['books']