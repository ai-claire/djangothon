from django.shortcuts import render
from logger.models import Insight
from django.conf import settings
import imgkit
# Create your views here.
from django.http import HttpResponse
import os
import json
import numpy as np
import ast
import cv2


def index(request):
    return render(request,"test2.html", {'js_id': 'blog_content'})

def metrics(request):
    metric_id = request.GET.get('metric_id', '')
    insight = Insight.objects.get(id=metric_id)
    html_content = ''
    # image_np = imgkit.from_url(insight.url, False, options={'width': insight.dimensionX})
    # nparr = np.fromstring(image_np, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    with open(os.path.join(settings.BASE_DIR, 'media', insight.html_filename), 'r') as f:
        html_content = f.read()

    # col_values = np.zeros(img.shape[0])
    # ins = ast.literal_eval(insight.insights)
    # for item in ins:
    #     col_values[item['scrollPos']:max(item['scrollPos'] + insight.dimensionY, img.shape[0])] += item.endTime
    # current_elt = 0
    # current_val = col_values[0]
    # d = {}
    # for i in len(col_values):
    #     item = col_values[i]
    #     if current_val != item:
    #         d[current_elt] = current_val
    #         current_elt = i
    #         current_val = item
    # d[current_elt] = current_val
    # k = d.keys()m  'keys': k, 'mets': d

    return render(request, 'metrics.html', {'dimensionX': insight.dimensionX,
        'dimensionY': insight.dimensionY, 'html_content': html_content,})