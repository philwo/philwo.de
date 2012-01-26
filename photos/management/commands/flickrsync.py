# -*- coding: utf-8 -*-

import os
import os.path
import urllib
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

import flickrapi

from photos.models import *


def sync(ist, soll, add_func=None, delete_func=None, modify_func=None):
    for s in soll:
        if s not in ist:
            # Soll, aber ist nicht
            if add_func != None:
                add_func(s)
        else:
            # Soll und ist auch :)
            pass
    for i in ist:
        if i not in soll:
            # Ist, aber soll nicht
            if delete_func != None:
                delete_func(i)
    for i in ist:
        if i in soll:
            # Ist und soll auch
            if modify_func != None:
                modify_func(i)


class Command(BaseCommand):
    help = ('Syncs photos from flickr')
    requires_model_validation = True
    can_import_settings = True

    def add_photoset(self, ps_id):
        print "Add / Modify: %s" % (ps_id,)
        ps_xml = self.flickr.photosets_getInfo(photoset_id=ps_id)[0]
        assert ps_xml.attrib['id'] == ps_id
        try:
            ps = Photoset.objects.get(pk=ps_id)
        except Photoset.DoesNotExist:
            ps = Photoset()
            ps.id = ps_xml.attrib['id']
        ps.primary = ps_xml.attrib['primary']
        ps.secret = ps_xml.attrib['secret']
        ps.server = ps_xml.attrib['server']
        ps.farm = ps_xml.attrib['farm']
        ps.photo_count = ps_xml.attrib['photos']
        ps.title = ps_xml[0].text
        ps.slug = slugify(ps.title.lower().replace(u'ä', u'ae').replace(u'ü', u'ue').replace(u'ö', u'oe'))
        ps.description = ps_xml[1].text or ''
        ps.order = ps.order or 0
        ps.save()

        photos_xml = self.flickr.photosets_getPhotos(photoset_id=ps_id, extras='original_format,o_dims,date_taken')[0]
        photo_ids = []
        for photo_xml in photos_xml:
            print "- Adding photo %s to set" % (photo_xml.attrib['id'],)
            try:
                photo = Photo.objects.get(pk=photo_xml.attrib['id'])
            except Photo.DoesNotExist:
                photo = Photo()
                photo.id = photo_xml.attrib['id']
            photo.secret = photo_xml.attrib['secret']
            photo.server = photo_xml.attrib['server']
            photo.farm = photo_xml.attrib['farm']
            photo.title = photo_xml.attrib['title']
            photo.originalsecret = photo_xml.attrib['originalsecret']
            photo.originalformat = photo_xml.attrib['originalformat']
            photo.o_width = photo_xml.attrib['o_width']
            photo.o_height = photo_xml.attrib['o_height']
            photo.date_taken = datetime.strptime(photo_xml.attrib['datetaken'], '%Y-%m-%d %H:%M:%S')
            photo.save()
            photo_ids.append(photo.id)
        ps.photos = photo_ids
        ps.save()

    def modify_photoset(self, ps_id):
        self.add_photoset(ps_id)

    def delete_photoset(self, ps_id):
        print "Delete: %s" % (ps_id,)
        Photoset.objects.delete(pk=ps_id)

    def handle(self, *args, **kwargs):
        api_key = getattr(settings, 'FLICKR_API_KEY', None)
        user_id = getattr(settings, 'FLICKR_USER_ID', None)

        from django.core.cache import cache
        self.flickr = flickrapi.FlickrAPI(api_key)
        self.flickr.cache = cache

        photosets = self.flickr.photosets_getList(user_id=user_id)[0]

        flickr_ids = [ps.attrib['id'] for ps in photosets]
        db_ids = list(Photoset.objects.values_list('id', flat=True))
        sync(db_ids, flickr_ids, self.add_photoset, self.delete_photoset, self.modify_photoset)

        # Sort sets by flickr-order
        order = 1
        for id in flickr_ids:
            ps = Photoset.objects.get(pk=id)
            ps.order = order
            ps.save()
            order += 1

        # Generate thumbnails
        originals_dir = os.path.join(settings.MEDIA_ROOT, 'photos', 'originals')
        gallery_dir = os.path.join(settings.MEDIA_ROOT, 'photos', 'gallery')
        thumbnails_dir = os.path.join(settings.MEDIA_ROOT, 'photos', 'thumbnails')
        if not os.path.isdir(originals_dir):
            os.makedirs(originals_dir)
        if not os.path.isdir(gallery_dir):
            os.makedirs(gallery_dir)
        if not os.path.isdir(thumbnails_dir):
            os.makedirs(thumbnails_dir)
        for photo in Photo.objects.all():
            original_path = os.path.join(originals_dir, photo.id) + '.' + photo.originalformat
            gallery_path = os.path.join(gallery_dir, photo.id) + '.jpg'
            thumbnail_path = os.path.join(thumbnails_dir, photo.id) + '.jpg'

            if not os.path.isfile(original_path):
                try:
                    urllib.urlretrieve(photo.get_flickr_original_url(), original_path)
                except urllib.ContentTooShortError:
                    if os.path.isfile(original_path):
                        os.unlink(original_path)
                    raise e

            if not os.path.isfile(gallery_path):
                resize_arg = ["-resize", "960x540"]

                try:
                    convert_app = '/usr/local/bin/convert'
                    if not os.path.isfile(convert_app):
                        convert_app = '/usr/bin/convert'
                    args = [convert_app, original_path] + resize_arg + ['-unsharp', '2x1+0.2+0', '-compress', 'JPEG', '-quality', '90', '-sampling-factor', '1x1', gallery_path]
                    subprocess.check_call(args)
                except subprocess.CalledProcessError, e:
                    if os.path.isfile(gallery_path):
                        os.unlink(gallery_path)
                    raise e
                except IOError, e:
                    if os.path.isfile(gallery_path):
                        os.unlink(gallery_path)
                    raise e

            if not os.path.isfile(thumbnail_path):
                cur_width, cur_height = (photo.o_width, photo.o_height)
                new_width, new_height = (280, 195)
                ratio = max(float(new_width) / cur_width, float(new_height) / cur_height)
                x = (cur_width * ratio)
                y = (cur_height * ratio)
                resize_arg = ["-resize", "%sx%s" % (int(x), int(y)), "+repage", "-gravity", "Center", "-crop", "%sx%s+0+0" % (new_width, new_height), "+repage"]

                try:
                    convert_app = '/usr/local/bin/convert'
                    if not os.path.isfile(convert_app):
                        convert_app = '/usr/bin/convert'
                    args = [convert_app, original_path] + resize_arg + ['-unsharp', '2x1+0.2+0', '-compress', 'JPEG', '-quality', '90', '-sampling-factor', '1x1', thumbnail_path]
                    subprocess.check_call(args)
                except subprocess.CalledProcessError, e:
                    if os.path.isfile(thumbnail_path):
                        os.unlink(thumbnail_path)
                    raise e
                except IOError, e:
                    if os.path.isfile(thumbnail_path):
                        os.unlink(thumbnail_path)
                    raise e
