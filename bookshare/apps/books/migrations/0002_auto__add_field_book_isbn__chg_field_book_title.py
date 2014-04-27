# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Book.isbn'
        db.add_column(u'books_book', 'isbn',
                      self.gf('django.db.models.fields.CharField')(default='0000000000000', max_length=13),
                      keep_default=False)


        # Changing field 'Book.title'
        db.alter_column(u'books_book', 'title', self.gf('django.db.models.fields.CharField')(max_length=80))

    def backwards(self, orm):
        # Deleting field 'Book.isbn'
        db.delete_column(u'books_book', 'isbn')


        # Changing field 'Book.title'
        db.alter_column(u'books_book', 'title', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'books.book': {
            'Meta': {'object_name': 'Book'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['books']