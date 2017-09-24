from django.conf.urls import url
from blog import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^time/', views.time)   
]