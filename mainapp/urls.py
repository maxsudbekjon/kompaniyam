from django.urls import path
from . import views

urlpatterns = [
  path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
  path('about/', views.AboutDataView.as_view(), name='about_data'),
  path('services/', views.ServiceView.as_view(), name='services'),
  path('portfolie-projects/', views.PortfolieProjectsView.as_view(), name='portfolie_projects'),
  path('comments/', views.CommentView.as_view(), name='comments'),
]