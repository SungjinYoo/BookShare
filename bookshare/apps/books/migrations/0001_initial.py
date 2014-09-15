# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'books_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2014)),
            ('semester', self.gf('django.db.models.fields.CharField')(default=u'second', max_length=10, blank=True)),
        ))
        db.send_create_signal(u'books', ['Course'])

        # Adding model 'Book'
        db.create_table(u'books_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'books', ['Book'])

        # Adding M2M table for field courses on 'Book'
        m2m_table_name = db.shorten_name(u'books_book_courses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'books.book'], null=False)),
            ('course', models.ForeignKey(orm[u'books.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'course_id'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'books_course')

        # Deleting model 'Book'
        db.delete_table(u'books_book')

        # Removing M2M table for field courses on 'Book'
        db.delete_table(db.shorten_name(u'books_book_courses'))


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
            'department': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'default': "u'second'", 'max_length': '10', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2014'})
        }
    }

    complete_apps = ['books']