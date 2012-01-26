# -*- coding: utf-8 -*-

from django.contrib import admin

from base.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
