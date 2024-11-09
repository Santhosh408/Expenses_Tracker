from rest_framework.serializers import ModelSerializer,CharField
from django.contrib.auth.models import User
from .models import Expenses

class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password']

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            )
        return user
    
    def update(self,instance,validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.save()
        return instance
        
class ExpensesSerializer(ModelSerializer):
    username = CharField(source='user.username',read_only=True)
    class Meta:
        model = Expenses
        fields = '__all__'
        read_only_fields = ['user']