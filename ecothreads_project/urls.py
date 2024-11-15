from django.contrib import admin
from django.urls import path, include
from payments.views import process_payment, mpesa_callback, check_payment_status_view
from api import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls')),
    path('mpesa_callback/', mpesa_callback, name='mpesa_callback'),
    path('process_payment/', process_payment, name='process_payment'),
    path('check_payment_status/', check_payment_status_view, name='check_payment_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
