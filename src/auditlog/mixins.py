import json

from django.conf import settings
from django.core import urlresolvers
try:
    from django.urls.exceptions import NoReverseMatch
except ImportError:
    from django.core.urlresolvers import NoReverseMatch

MAX = 75


class LogEntryAdminMixin(object):

    def created(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    created.short_description = 'Created'

    def user_url(self, obj):
        if obj.actor:
            app_label, model = settings.AUTH_USER_MODEL.split('.')
            viewname = 'admin:%s_%s_change' % (app_label, model.lower())
            link = urlresolvers.reverse(viewname, args=[obj.actor.id])
            return u'<a href="%s">%s</a>' % (link, obj.actor)

        return 'system'
    user_url.allow_tags = True
    user_url.short_description = 'User'

    def resource_url(self, obj):
        app_label, model = obj.content_object._meta.app_label, obj.content_object._meta.model_name
        viewname = 'admin:%s_%s_change' % (app_label, model)
        id = obj.object_id
        if obj.object_id is None:
            id = obj.object_pk
        try:
            link = urlresolvers.reverse(viewname, args=[id])
        except NoReverseMatch:
            return obj.object_repr
        else:
            return u'<a href="%s">%s</a>' % (link, obj.object_repr)
    resource_url.allow_tags = True
    resource_url.short_description = 'Resource'

    def related_resource_url(self, obj):
        if obj.related_object:
            app_label, model = obj.related_object._meta.app_label, obj.related_object._meta.model_name
            viewname = 'admin:%s_%s_change' % (app_label, model)
            id = obj.related_object_pk
            try:
                link = urlresolvers.reverse(viewname, args=[id])
            except NoReverseMatch:
                return obj.object_repr
            else:
                return u'<a href="%s">%s</a>' % (link, obj.related_object)
    related_resource_url.allow_tags = True
    related_resource_url.short_description = 'Related Resource'

    def msg_short(self, obj):
        if obj.action == 2:
            return ''  # delete
        changes = json.loads(obj.changes)
        s = '' if len(changes) == 1 else 's'
        fields = ', '.join(changes.keys())
        if len(fields) > MAX:
            i = fields.rfind(' ', 0, MAX)
            fields = fields[:i] + ' ..'
        return '%d change%s: %s' % (len(changes), s, fields)
    msg_short.short_description = 'Changes'

    def msg(self, obj):
        if obj.action == 2:
            return ''  # delete
        changes = json.loads(obj.changes)
        msg = '<table><tr><th>#</th><th>Field</th><th>From</th><th>To</th></tr>'
        for i, field in enumerate(sorted(changes), 1):
            value = [i, field] + (['***', '***'] if field == 'password' else changes[field])
            msg += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(value)
        msg += '</table>'
        return msg
    msg.allow_tags = True
    msg.short_description = 'Changes'
