# make it compatible to django 1.10
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
import re

from amp_tools.settings import settings
from amp_tools import set_amp_detect


class AMPDetectionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if settings.AMP_TOOLS_GET_PARAMETER in request.GET:
            if request.GET[settings.AMP_TOOLS_GET_PARAMETER] == settings.AMP_TOOLS_GET_VALUE:
                if settings.AMP_TOOLS_ACTIVE_URLS:
                    for url in settings.AMP_TOOLS_ACTIVE_URLS:
                        pattern_type = re._pattern_type if hasattr(re, '_pattern_type') else re.Pattern
                        if not isinstance(url, pattern_type):
                            url = str(url)
                        url_re = re.compile(url)

                        if url_re.match(request.path_info):
                            set_amp_detect(is_amp_detect=True, request=request)
                else:
                    set_amp_detect(is_amp_detect=True, request=request)
        else:
            set_amp_detect(is_amp_detect=False, request=request)
