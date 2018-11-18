import warnings
import django

from django.template.loader import get_template
from classytags.helpers import InclusionTag
from django import template
from django.template.loader import render_to_string


register = template.Library()

# tanya@botreveiw.com
# class LoggerJs(InclusionTag):
# 	"""
# 	Displays cookie law banner only if user has not dismissed it yet.
# 	"""

# 	template = 'logger/logger.html'

# 	def load_logger(self, context, **kwargs):
# 		template_filename = self.get_template(context, **kwargs)

# 		data = self.get_context(context, **kwargs)
# 		return render_to_string(template_filename, data, context.request)

# register.tag(LoggerJs)


# @register.inclusion_tag('logger/logger.html')
def load_logger(id):
	return {'js_id': id}

register.inclusion_tag(get_template('logger.html'))(load_logger)

