# -*- coding: utf-8 -*-

from lettuce import world

def delete_all_meetmes():
    confrooms = world.ws.confrooms.list()
    for confroom in confrooms:
        world.ws.confrooms.delete(confroom.id)

def delete_meetme_with_confno(confno):
    for meetme in _search_meetmes_by_confno(confno):
        world.ws.confrooms.delete(meetme.id)


def _search_meetmes_by_confno(confno):
    return world.ws.confrooms.search_by_number(confno)
