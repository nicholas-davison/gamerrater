from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category


class GameViewSet(ViewSet):
    """game view set"""

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    categories = CategorySerializer(many=True)
    #categories = serializers.StringRelatedField(many=True, source='categories.all')
    class Meta:
        model = Game
        fields = [ 'id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_play_time', 'age_recommendation', 'categories' ]

