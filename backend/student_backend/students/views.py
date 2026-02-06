from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.db.models import Q

@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_student(request, id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return Response({'message': 'Deleted'})

@api_view(['GET'])
def search_students(request):
    keyword = request.GET.get('q')
    students = Student.objects.filter(
        Q(name__icontains=keyword) |
        Q(address__icontains=keyword) |
        Q(age__icontains=keyword) |
        Q(id__icontains=keyword)
    )
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def count_students(request):
    total = Student.objects.count()
    return JsonResponse({"count": total})