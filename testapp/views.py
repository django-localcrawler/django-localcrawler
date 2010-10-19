from django.shortcuts import render_to_response
from django.template.context import RequestContext


class RenderTemplate(object):
    def __init__(self, template=None):
        self.template = template
        
    def __call__(self, request, **kwargs):
        template = self.template or '%s.html' % kwargs['template']
        return render_to_response(template, {}, RequestContext(request))