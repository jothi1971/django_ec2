from rest_framework import serializers
from .models import * 
"""convert JSON to models. one serialiser for each model"""
class ProjectSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Project
        fields = ('id','name','projectmanager', 'start_date','employees', 'end_date', 'comments', 'status')


class ProjectManagerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProjectManager
        fields = ('name', 'id')
 

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Employees
        fields = ('name', 'id')