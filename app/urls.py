from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('car', views.car),
    path('car/<int:myid>', views.booking),
    path('contact', views.contact),
    path('service', views.service),
    path('team', views.team),
    path('testimonial', views.testimonial),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    path('accountinfo/', views.accinfo),
    path('search/', views.search, name='search'),
    path('Test/', views.test, name='search'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('handlerequest/', views.handlerequest, name="handlerequest"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)