from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from disease.api.serializers import DiseasesSerializer
from disease.models import Disease


class Diseases(APIView):
    def get(self, request):
        disease = Disease.objects.all()
        serializer = DiseasesSerializer(
            disease, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = DiseasesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
 

class DiseasesDetailAV(APIView):

    def get(self, request, pk):
        try:
            platform = Disease.objects.get(pk=pk)
        except Disease.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiseasesSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = Disease.objects.get(pk=pk)
        serializer = DiseasesSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = Disease.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)