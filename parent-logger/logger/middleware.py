from .models import Insight
import json


import cv2
from matplotlib import pyplot as plt
import imgkit
import json
import numpy as np
from pprint import pprint
from PIL import Image
from threading import Thread
import os
import uuid
import lzstring
import matplotlib
from django.conf import settings
from bs4 import BeautifulSoup
import requests

def generate_image(insight):
	# image_np = imgkit.from_url(insight['url'], False, options={'width': insight['dimensionX'], 'format': 'png'})
	insight['insights'] = json.loads(insight['insights'])
	# nparr = np.fromstring(image_np, np.uint8)
	# img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

	# col_values = np.zeros(insight['height'])
	# for item in insight['insights']:
	# 	col_values[item['scrollPos']:max(item['scrollPos'] + insight['dimensionY'], img['height'])] += item['endTime']

	# max_intensity = np.amax(col_values)
	# col_values /= max_intensity
	# col_values = cv2.merge([col_values * 255, col_values * 255, col_values * 255, np.ones(col_values.shape) * 255])
	# col_values = np.repeat(col_values, insight['dimensionX'], axis=1)
	# col_values = col_values.astype(np.uint8)

	col_values = np.zeros(insight['height'])
	for item in a['insights']:
		col_values[item['scrollPos']:max((item['scrollPos'] + a['dimensionY']), insight['height'])] += item['endTime']

	max_intensity = np.amax(col_values)

	col_values /= max_intensity

	# set levels
	# unique = np.unique(col_values)
	# unique.sort()

	# for i in range(len(unique)):
	#     col_values[col_values == unique[i]] = i


	# col_values = (col_values / max(len(unique-1), 1))
	temp_col_values = 1 - col_values
	temp_col_values = cv2.merge([temp_col_values * 255, temp_col_values * 255, temp_col_values * 255, np.ones(temp_col_values.shape) * 255])
	temp_col_values = np.repeat(temp_col_values, insight['dimensionX'], axis=1)
	temp_col_values = temp_col_values.astype(np.uint8)

	# added = cv2.addWeighted(img, 0.6, temp_col_values, 0.4, 0)
	return temp_col_values



def generate_image_for_insight(insight):
	filename = "%s" % (uuid.uuid4())
	img_filename = filename + '.png'
	html_filename = filename + '.html'
	dir_path = os.path.join(settings.BASE_DIR, 'media')
	try:
		dir_path = settings.LOGGER_IMAGES_DIR
	except:
		pass

	cv2.imwrite(os.path.join(dir_path, img_filename), generate_image(insight.__dict__))
	# matplotlib.image.imsave(os.path.join(dir_path, filename), generate_image(insight.__dict__))
	page = requests.get(insight.url)
	soup = BeautifulSoup(page.content, 'html.parser')
	c = soup.find(id='blog_content')

	c['style'] += ';background-image: url("http://localhost:8000/media/' + img_filename + '");'

	html = soup.prettify('utf-8')

	with open(os.path.join(dir_path, html_filename), 'wb') as f:
		f.write(html)

	insight.file_name = img_filename
	insight.html_filename = html_filename

	insight.save()



class LoggerMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		cookie_insight = request.COOKIES.get('logger_insight', '')
		response = self.get_response(request)
		if cookie_insight:
			try:
				# t = json.loads(lzstring.LZString().decompressFromBase64(cookie_insight))
				t = json.loads(cookie_insight)
				print('intercepted: ', t)
				ins = Insight(dimensionX=t.get('dimensionX', 360),
				dimensionY=t.get('dimensionY', 1080), url=t.get('url', ''),
				insights=json.dumps(t.get('insights', []), height=t.get('height', 100)))
				ins.save()
				t = Thread(target=generate_image_for_insight, args=(ins,))
				t.start()
			except Exception as e:
				print('Error at middleware: ', e)
			response.set_cookie('logger_insight', '')
		return response