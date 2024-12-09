from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from .models import *
from .GeneAI import create_content
import Craigs_US.usa_main as usa
import Craigs_india.india_main as india
import globals

# def home(request): 
#     return HttpResponse("This is the homepage")
class ScrapViewset(viewsets.ViewSet):
  
    def create(self, request):
        print('jothi keywords ', request.data)
        #globals.search_keywords = request.data['keywords'].split()
        print("jothi scrap list")
        usa.usamain()
        #india.indiamain()
        return HttpResponse("scrap response ")
       
class ContentViewset(viewsets.ViewSet):
    print("Content viewset called")

    def list(self, request):
        print("jothi content list")
        return HttpResponse("content response ")
        
    def create(self, request): 
        print("jothi create content " + str(request.data))
        return HttpResponse(create_content(request.data['model'],request.data['content']))

    
class ProjectManagerViewset(viewsets.ViewSet):
    print("projectmanager viewset called")
    permission_classes = [permissions.AllowAny]
    queryset = ProjectManager.objects.all()
    serializer_class = ProjectManagerSerializer

    def list(self, request):
        print("projectmanager viewset list")
        queryset = ProjectManager.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class EmployeesViewset(viewsets.ViewSet):
    print("EmployeesViewset viewset called")
    permission_classes = [permissions.AllowAny]
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer

    def list(self, request):
        print("employee viewset list")
        queryset = Employees.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ProjectViewset(viewsets.ViewSet):
    print("ProjectViewset viewset called")
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        print("project viewset list")
        queryset = Project.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        print("project viewset create")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        print("project viewset retrive")
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        print("project viewset update")
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project,data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        print("project viewset destroy")
        project = self.queryset.get(pk=pk)
        project.delete()
        return Response(status=204)
        




