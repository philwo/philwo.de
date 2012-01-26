# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from models import Photoset, Photo


def galleries(request):
    photosets = Photoset.objects.all()
    return render(request, 'photos/galleries.html', {'photosets': photosets})


def gallery(request, slug):
    photoset = get_object_or_404(Photoset, slug=slug)
    return render(request, 'photos/gallery.html', {'photoset': photoset})


def photo(request, id):
    photo = get_object_or_404(Photo, pk=id)
    return render(request, 'photos/photo.html', {'photo': photo})
