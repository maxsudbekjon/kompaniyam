from django.urls import path
from . import views

urlpatterns = [
  path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
  path('about/', views.AboutDataView.as_view(), name='about_data'),
  path('services/', views.ServiceView.as_view(), name='services'),
  path('portfolio-projects/', views.PortfolieProjectsView.as_view(), name='portfolio_projects'),
  path('comments/', views.CommentView.as_view(), name='comments'),
  path('project-suggestions/', views.ProjectSuggestionView.as_view(), name='project_suggestions'),
  path('comment_p/', views.CommentViewWithProject.as_view(), name='comment-p')
]