from django.conf.urls import url
from transtool.views import LocaleMessagesExportView


urlpatterns = [
    url(r'^localemessages/export/$', LocaleMessagesExportView.as_view(), name='localemessages_export'),
]
