from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category
from django.contrib.auth.models import User


class GameViewSet(ViewSet):
    """game view set"""

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, many=False)
            return Response(serializer.data)
        
        except Game.DoesNotExist:
                return Response({'Response': 'The game you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        # extract fields from request
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        designer = request.data.get('designer', None)
        year = request.data.get('year_released', None)
        players = request.data.get('number_of_players', None)
        time = request.data.get('estimated_play_time', None)
        age = request.data.get('age_recommendation', None)
        user = request.auth.user

        if title is None or description is None or designer is None or year is None or players is None or time is None or age is None:
            return Response({'Message': 'You must include title, description, designer, year_released, number_of_players, estimated_play_time, and age_recommendation in your request'}, status=status.HTTP_400_BAD_REQUEST)
        
        #create an instance of the game class and update its property values with those of the request
        new_game = Game()
        new_game.user = user
        new_game.title = title
        new_game.description = description
        new_game.designer = designer
        new_game.year_released = year
        new_game.number_of_players = players
        new_game.estimated_play_time = time
        new_game.age_recommendation = age

        #save in db
        new_game.save()

        #serialize the new object 
        serialized = GameSerializer(new_game, many=False)

        #return serialized response
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk): 
        # extract fields from client request
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        designer = request.data.get('designer', None)
        year = request.data.get('year_released', None)
        players = request.data.get('number_of_players', None)
        time = request.data.get('estimated_play_time', None)
        age = request.data.get('age_recommendation', None)

        if title is None or description is None or designer is None or year is None or players is None or time is None or age is None:
            return Response({'Message': 'You must include title, description, designer, year_released, number_of_players, estimated_play_time, and age_recommendation in your request'}, status=status.HTTP_400_BAD_REQUEST)
        
        #instantiate an object from the specified row in db
        try:
            game_to_update = Game.objects.get(pk=pk)
        #update columns with request data
            game_to_update.title = title
            game_to_update.description = description
            game_to_update.designer = designer
            game_to_update.year_released = year
            game_to_update.number_of_players = players
            game_to_update.estimated_play_time = time
            game_to_update.age_recommendation = age
        #save new row
            game_to_update.save()
        #return success with no response body
            return Response({"message": "game successfully updated"}, status=status.HTTP_204_NO_CONTENT)
        
        except Game.DoesNotExist:
                return Response({'Response': 'The game you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk):
        try:
             game_to_delete = Game.objects.get(pk=pk)
             game_to_delete.delete()
             return Response({'message': 'successfully terminated game'}, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist:
             return Response({'message': 'failure to locate game to destroy'}, status=status.HTTP_404_NOT_FOUND)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
        

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    categories = CategorySerializer(many=True)
    class Meta:
        model = Game
        fields = [ 'id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_play_time', 'age_recommendation', 'categories' ]