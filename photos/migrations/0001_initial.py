# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Photo'
        db.create_table('photos_photo', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('farm', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('originalsecret', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('originalformat', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('o_width', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('o_height', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('photos', ['Photo'])

        # Adding model 'Photoset'
        db.create_table('photos_photoset', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('primary', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('farm', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo_count', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('photos', ['Photoset'])

        # Adding M2M table for field photos on 'Photoset'
        db.create_table('photos_photoset_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photoset', models.ForeignKey(orm['photos.photoset'], null=False)),
            ('photo', models.ForeignKey(orm['photos.photo'], null=False))
        ))
        db.create_unique('photos_photoset_photos', ['photoset_id', 'photo_id'])


    def backwards(self, orm):
        
        # Deleting model 'Photo'
        db.delete_table('photos_photo')

        # Deleting model 'Photoset'
        db.delete_table('photos_photoset')

        # Removing M2M table for field photos on 'Photoset'
        db.delete_table('photos_photoset_photos')


    models = {
        'photos.photo': {
            'Meta': {'ordering': "['date_taken']", 'object_name': 'Photo'},
            'date_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'farm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'o_height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'o_width': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'originalformat': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'originalsecret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'photos.photoset': {
            'Meta': {'ordering': "['order']", 'object_name': 'Photoset'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'farm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'photo_count': ('django.db.models.fields.IntegerField', [], {}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['photos.Photo']", 'symmetrical': 'False'}),
            'primary': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['photos']
