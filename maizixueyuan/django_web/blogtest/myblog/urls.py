from django.conf.urls import url
from myblog import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^time/', views.time)   
]