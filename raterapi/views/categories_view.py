from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Category, Game
from django.contrib.auth.models import User

class CategoryViewSet(ViewSet):

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class GameSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title',)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""
    games = GameSeralizer(many=True)

    class Meta:
        model = Category
        fields = ( 'id', 'name', 'games' )