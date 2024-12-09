from django.urls import path 
from .views import * 
from rest_framework.routers import DefaultRouter

""" urls are automatically created """
router = DefaultRouter()
"""project/ and project/pk"""
router.register('project', ProjectViewset, basename='project')
router.register('projectmanager', ProjectManagerViewset, basename='projectmanager')
router.register('employees', EmployeesViewset, basename='employees')
router.register('content', ContentViewset, basename='content')
router.register('scrap', ScrapViewset, basename='scrap')

urlpatterns = router.urls


# urlpatterns = [
#     path('', home)
# ]