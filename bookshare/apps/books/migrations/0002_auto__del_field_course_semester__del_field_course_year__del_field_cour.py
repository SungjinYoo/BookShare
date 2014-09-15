# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.semester'
        db.delete_column(u'books_course', 'semester')

        # Deleting field 'Course.year'
        db.delete_column(u'books_course', 'year')

        # Deleting field 'Course.department'
        db.delete_column(u'books_course', 'department')


    def backwards(self, orm):
        # Adding field 'Course.semester'
        db.add_column(u'books_course', 'semester',
                      self.gf('django.db.models.fields.CharField')(default=u'second', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Course.year'
        db.add_column(u'books_course', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=2014),
                      keep_default=False)

        # Adding field 'Course.department'
        db.add_column(u'books_course', 'department',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


    models = {
        u'books.book': {
            'Meta': {'object_name': 'Book'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['books.Course']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'books.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['books']