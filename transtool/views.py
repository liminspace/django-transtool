import zipfile
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http.response import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .tools import get_lc_files_list
from .settings import TRANSTOOL_EXPORT_KEY, TRANSTOOL_PROJECT_BASE_DIR


class LocaleMessagesExportView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LocaleMessagesExportView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not TRANSTOOL_EXPORT_KEY or request.POST.get('key') != TRANSTOOL_EXPORT_KEY:
            raise PermissionDenied
        if request.POST.get('po-only') == '1':
            exts = ['.po']
        elif request.POST.get('mo-only') == '1':
            exts = ['.mo']
        else:
            exts = ['.po', '.mo']
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="localemessages.zip"'
        z = zipfile.ZipFile(response, 'w', compression=zipfile.ZIP_DEFLATED)
        try:
            for abs_path, rel_path in get_lc_files_list(TRANSTOOL_PROJECT_BASE_DIR, exts=exts):
                with open(abs_path, 'rb') as tf:
                    z.writestr(rel_path, tf.read())
        finally:
            z.close()
        return response

    def get(self, request, *args, **kwargs):
        raise Http404
