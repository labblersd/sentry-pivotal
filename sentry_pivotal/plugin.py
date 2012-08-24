#!/usr/bin/env python
'''
Sentry-Pivotal
=============

License
-------
Copyright 2012 Labbler, Inc.

This file is part of Sentry-Pivotal.

Sentry-Pivotal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sentry-Pivotal is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sentry-Pivotal.  If not, see <http://www.gnu.org/licenses/>.
'''
from django import forms

from sentry.conf import settings
from sentry.plugins import Plugin

from pyvotal import PTracker
import sentry_pivotal

class PivotalSettingsForm(forms.Form):
    token = forms.CharField(label='Pivotal Tracker Access Token', required=True)
    project = forms.IntegerField(label='Project ID', required=True)
    #vonni_receiver = forms.CharField(label='Vonni Receiver')

class PivotalStory(Plugin):

    version = sentry_pivotal.VERSION
    project_conf_form = PivotalSettingsForm

    def can_enable_for_projects(self):
        return True

    def is_setup(self, project):
        return (
            all((self.get_option(key, project)
                for key in ('token', 'project'))
            )
        )

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if not is_new or not self.is_setup(event.project):
            return

        name = '[SENTRY]:%s: %s at %s' % (event.get_level_display().upper(),
                            event.error().split('\n')[0], event.project)

        link = '%s/%s/group/%d/' % (settings.URL_PREFIX, group.project.slug,
                                    group.id)

        message = 'Server: %s\n' % event.server_name
        message += 'Group: %s\n' % event.group
        message += 'Logger: %s\n' % event.logger
        message += 'Message: %s\n' % event.message
        message += '\n%s\n' % link

        self.make_story(name, message, event)

    def make_story(self, name, message, event):
        print self.get_option('token', event.project)
        ptracker = PTracker(token=self.get_option('token', event.project))
        story = ptracker.Story()
        story.type = "bug"
        story.name = name
        story.labels = "sentry"
        project = ptracker.projects.get(self.get_option('project', event.project))
        story = project.stories.add(story)

