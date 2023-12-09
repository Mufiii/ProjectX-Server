from django.shortcuts import render
from .models import Workspace
from .serializers import(
  WorkSpaceListSerializer,
  WorkSpacePostSerializer
)
from rest_framework import status
from rest_framework.views import APIView
from vendor.models import BusinessVendor
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q



class WorkSpaceListCreateAPiView(APIView):
    permission_classes = (IsAuthenticated,)
  
    def get(self,request):
        worksapce = Workspace.objects.filter(vendor=request.user.vendor_profile)
        serializer = WorkSpaceListSerializer(worksapce, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self,request):
        serializer = WorkSpaceListSerializer(data=request.data)
        if serializer.is_valid():
            workspace = Workspace.objects.create(
            vendor = request.user.vendor_profile,
            name = serializer.validated_data['name'],
            description = serializer.validated_data['description']
            )
            workspace.save()
            return Response(
                {"data":serializer.data},status=status.HTTP_201_CREATED
            )
        return Response(
                {"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST
        )


class WorkSpaceGetUpdateAPIView(APIView):
    def get(self, request, pk):
        try:
            workspace = Workspace.objects.get(pk=pk, vendor__user__id=request.user.id)
            serializer = WorkSpacePostSerializer(workspace)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Workspace.DoesNotExist:
            return Response({"error": "Workspace not found"}, status=status.HTTP_404_NOT_FOUND)

    
    def put(self,request,pk):
        workspace = Workspace.objects.get(pk=pk, vendor__user__id=request.user.id)
        print(workspace)
        serializer = WorkSpacePostSerializer(
            workspace,data=request.data,partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(
            {"msg":"There is an error"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def delete(self,request,pk):
        workspace = Workspace.objects.get(pk=pk, vendor__user__id=request.user.id)
        workspace.delete()
        return Response(
            {"msg":"Workspace deleted Successfully"},
            status=status.HTTP_200_OK
        )
             