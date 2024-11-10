from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from .serializers import UserSerializer, ExpensesSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import Expenses
from django.http import Http404
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Sum

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'User Created Successfully'},status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        username,password = data.get('username'),data.get('password')
        if not username or not password:
            Response({'Error':'username and password are required'},status=HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User,username=username)
        if not user.check_password:
            return Response({'Error':'Plese Enter the correct password'},status=HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance=user)
        token,created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key,'data':serializer.data})
    
class LogoutView(APIView):
    def post(self,request):
        user = request.user
        try:
            user.auth_token.delete()
            return Response({'Message':'Logged out successfully'},status=HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'Error':'Token Not found'},status=HTTP_400_BAD_REQUEST)
             
class UserUpdateView(APIView):
    def put(self,request):
        user = request.user
        data = request.data
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'User Updated Successfully'},status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class ExpensesView(APIView):
    def get(self,request):
        expenses = Expenses.objects.filter(user=request.user)
        serializer = ExpensesSerializer(expenses,many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        serializer = ExpensesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"Message":"Expenses Added Successfully"},status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class ExpensesDetailView(APIView):
    def get_object(self,pk):
        try:
            return Expenses.objects.get(user=self.request.user,pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        expense = self.get_object(pk)
        serializer = ExpensesSerializer(expense)
        return Response(serializer.data,status=HTTP_200_OK)
    
    def put(self,request,pk):
        expense = self.get_object(pk)
        serializer = ExpensesSerializer(expense,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        expense = self.get_object(pk)
        serializer = ExpensesSerializer(expense,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        expense = self.get_object(pk)
        expense.delete()
        return Response({"message":"Expense_deleted"},status=HTTP_200_OK)
    
class MonthlyExpenseSummeryView(APIView):
    def get(self,request):
        user = request.user
        current_year = timezone.now().year
        monthly_expenses = (
            Expenses.objects.filter(user=user, date__year=current_year)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )
        return Response(monthly_expenses,status=HTTP_200_OK)
    