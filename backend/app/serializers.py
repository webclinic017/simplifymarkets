from rest_framework import serializers
from . models import employee, knowledge
from django.contrib.auth.models import User

class employeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = employee
        fields = '__all__'

class knowledgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = knowledge
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']