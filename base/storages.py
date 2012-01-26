# -*- coding: utf-8 -*-

import os

from django.core.files.storage import FileSystemStorage

from PIL import ImageFile as PILImageFile


class OverwriteStorage(FileSystemStorage):
    """
    Based on http://bitbucket.org/david/django-storages/src/85e72f47f638/storages/backends/overwrite.py

    See also Django #4339, which might add this functionality to core.
    """

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        if self.exists(name):
            self.delete(name)
        return name


class OverwriteImageStorage(OverwriteStorage):
    """
    Based on http://bitbucket.org/david/django-storages/src/85e72f47f638/storages/backends/image.py
    """

    def find_extension(self, format):
        """Normalizes PIL-returned format into a standard, lowercase extension."""
        format = format.lower()

        if format == 'jpeg':
            format = 'jpg'

        return format

    def save(self, name, content):
        dirname = os.path.dirname(name)
        basename = os.path.basename(name)

        # Use PIL to determine filetype
        p = PILImageFile.Parser()
        while 1:
            data = content.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                im = p.image
                break

        extension = self.find_extension(im.format)

        # Does the basename already have an extension? If so, replace it.
        # bare as in without extension
        bare_basename, _ = os.path.splitext(basename)
        basename = bare_basename + '.' + extension

        name = os.path.join(dirname, basename)
        return super(OverwriteStorage, self).save(name, content)
