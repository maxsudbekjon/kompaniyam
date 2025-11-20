from django.contrib import admin
from .models import AnalyticsModel, AboutDataModel, ServiceModel, PortfolieProjectsModel, CommentModel, ProjectSuggestionModel  

# Register your models here.

admin.site.register(AnalyticsModel)
admin.site.register(AboutDataModel)
admin.site.register(ServiceModel)
admin.site.register(PortfolieProjectsModel)
admin.site.register(CommentModel)
admin.site.register(ProjectSuggestionModel)