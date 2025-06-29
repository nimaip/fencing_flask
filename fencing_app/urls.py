from django.urls import path
from . import vercel_views

urlpatterns = [
    path('', vercel_views.home, name='home'),
    path('analyze/', vercel_views.analyze_pose, name='analyze_pose'),
] 