from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.course.models import Course
from apps.course.seializers import CourseSerializer


class CourseView(GenericAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def post(self, request):
        course_serializer = self.get_serializer(data=request.data)

        if course_serializer.is_valid():
            course_serializer.save()
            return Response({"detail": "Course added"})
        return Response(course_serializer.errors)

    def get(self, request):
        data = CourseSerializer(self.get_queryset(), many=True)
        return Response(data=data.data)