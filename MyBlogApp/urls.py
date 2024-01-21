from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('loginApp.urls')),
    path('blog/', include('blogApp.urls')),
    path('', views.Index, name='index'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
