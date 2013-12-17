from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context, loader
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
import os,json

from weblisa.utils import method_restricted_to, is_ajax
from weblisa.settings import LISA_PATH

from BBox.modules.bbox import BBox

# Template system will be fixed with Django 1.7. Each plugin will be able to have his own templates
@login_required()
def index(request):

    return render_to_response(os.path.abspath(os.path.dirname(__file__) + '/templates/bbox-index.html'),
                              {
                                  'content': 'test'
                              },
                              context_instance=RequestContext(request))
