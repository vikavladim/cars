from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from rest_framework import status, decorators
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CarForm, CommentForm
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from django.views.generic import View
from .models import Car, Comment


class CarListAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    @decorators.permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Ошибка сериализации:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    @decorators.permission_classes([IsAuthenticated])
    def put(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(car=car)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @decorators.permission_classes([IsAuthenticated])
    def post(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###################################

class CarListView(View):
    def get(self, request):
        car_list = Car.objects.all()
        return render(request, 'cars/car_list.html', {'cars': car_list})


class CarDetailView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        comments = car.comment_set.all()
        return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments})

    @method_decorator(login_required)
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(content=content, car=car, author=request.user)
            return redirect('car_detail', pk=pk)
        return render(request, 'cars/car_detail.html', {'car': car, 'error': 'Введите содержание комментария'})


class CarAddView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CarForm()
        return render(request, 'cars/car_create.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('car_detail', pk=car.pk)
        return render(request, 'cars/car_create.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class CarEditView(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return redirect('car_detail', pk=pk)
        form = CarForm(instance=car)
        return render(request, 'cars/car_edit.html', {'form': form})

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return redirect('car_detail', pk=pk)
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', pk=pk)
        return render(request, 'cars/car_edit.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class CarDeleteView(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return redirect('car_detail', pk=pk)
        return render(request, 'cars/car_delete.html')

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return redirect('car_detail', pk=pk)
        car.delete()
        return redirect('car_list')


class MyRecordsView(View):
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        cars = Car.objects.filter(owner=request.user)
        comments = Comment.objects.filter(author=request.user)
        return render(request, 'cars/my_records.html', {'cars': cars, 'comments': comments})
