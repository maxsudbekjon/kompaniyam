from django.contrib import admin
from .models import AnalyticsModel, AboutDataModel, ServiceModel, PortfolieProjectsModel, CommentModel

# Register your models here.

admin.site.register(AnalyticsModel)
admin.site.register(AboutDataModel)
admin.site.register(ServiceModel)
admin.site.register(PortfolieProjectsModel)
admin.site.register(CommentModel)