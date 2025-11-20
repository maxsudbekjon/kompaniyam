from django.shortcuts import render
from rest_framework.views import APIView
from .models import AnalyticsModel, AboutDataModel, ServiceModel, PortfolieProjectsModel, CommentModel
from .serializers import AnalyticsModelSerializer, AboutDataModelSerializer, ServiceModelSerializer, PortfolieProjectsModelSerializer, CommentModelSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from drf_spectacular.utils import extend_schema

class AnalyticsView(APIView):
    def get(self, request, *args, **kwargs):
        data = AnalyticsModel.objects.all().order_by('-id')
        serializer = AnalyticsModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AboutDataView(APIView):
    def get(self, request, *args, **kwargs):
        data = AboutDataModel.objects.all().order_by('-id')
        serializer = AboutDataModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class ServiceView(APIView):
    def get(self, request, *args, **kwargs):
        data = ServiceModel.objects.all().order_by('-id')
        serializer = ServiceModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class PortfolieProjectsView(APIView):
    def get(self, request, *args, **kwargs):
        data = PortfolieProjectsModel.objects.all().order_by('-id')
        serializer = PortfolieProjectsModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(request=CommentModelSerializer, responses=CommentModelSerializer)
class CommentView(APIView):
    def get(self, request, *args, **kwargs):
        data = CommentModel.objects.all().order_by('-id')
        serializer = CommentModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CommentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)