# -*- coding: utf-8 -*-
from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    style = models.CharField(max_length=100, choices=(
        (1, 'Rock'),
        (2, 'Funk'),
        (3, 'Jazz')
    ))
    agent = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)


class Musician(models.Model):
    band = models.ForeignKey(Band)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, choices=(
        (1, 'Vocal'),
        (2, 'Guitar'),
        (3, 'Bass'),
        (4, 'Drums')
    ))


class Concert(models.Model):
    band = models.ForeignKey(Band)
    location = models.CharField(max_length=100)
    date = models.DateField()


class Album(models.Model):
    band = models.ForeignKey(Band)
    name = models.CharField(max_length=100)
    date = models.DateField()


class Interview(models.Model):
    band = models.ForeignKey(Band)
    media_name = models.CharField(max_length=100)
    date = models.DateField()
