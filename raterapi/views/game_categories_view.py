from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameCategory
from django.contrib.auth.models import User

class GameCategoryViewSet(ViewSet):

    def create(self, request):
        #extract request fields
        game = request.data.get('game_id', None)
        category = request.data.get('category_id', None)

        if game is None or category is None:
            return Response({'message': 'please provide both a game and category'}, status=status.HTTP_400_BAD_REQUEST) 

        #instantiate GamesCategory
        new_game_category = GameCategory()

        #save request values to new instance of gamecategory
        new_game_category.game = game
        new_game_category.category = category

        #save to db
        new_game_category.save()

        #serialize
        serialized_game_category = GameCategorySerializer(new_game_category)

        #return response
        return Response(serialized_game_category.data, status=status.HTTP_201_CREATED)

class GameCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GameCategory
        fields = ['id', 'game', 'category']