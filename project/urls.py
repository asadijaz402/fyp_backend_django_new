from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.generic.base import TemplateResponseMixin
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('news/',views.Postdata.as_view()),
    path('news/<int:id>',views.Postdata.as_view()),
    path('list',views.get_trends.as_view()),

    # path('data/',views.PostView),


    # path('trends/',views.Trends.as_view())
    # path('',view.index,name='index')
    # path(r'',TemplateView.as_view(temlate_name='index.html')),

]


# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]