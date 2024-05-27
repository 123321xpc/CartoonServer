from django.urls import path
from imgs import views as img_views
from vdo import views as vdo_views

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('uploadimgs', img_views.upload_imgs, name='upload_imgs'),
    path('uploadvdo', vdo_views.upload_vdo, name='upload_vdo')
]
