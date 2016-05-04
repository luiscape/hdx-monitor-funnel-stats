#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
PATCH
-----

Patches data for the funnel stats application.
This is a horrendous hack: it simply deletes data
for the current week on a schedule (hourly).

    actually, I had a viewpoint: I was waiting for
    something extraordinary to
    happen

    -- Bukowski

'''
import scraperwiki as s
import datetime

def patch(week):
    '''
    Deletes entries from a target week.

    '''
    s.sql.execute('DELETE FROM funnel WHERE period="{week}"'.format(week=week))
    s.sql.execute('DELETE FROM funnel WHERE period="{week}"'.format(week=week))
    print 'Entries deleted for week: %s' % week

if __name__ == '__main__':
    d = datetime.datetime.now()
    patch(d.strftime('%Y-W%W'))