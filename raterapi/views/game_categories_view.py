from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameCategory, Game, Category
from django.contrib.auth.models import User

class GameCategoryViewSet(ViewSet):

    def create(self, request):
        #extract request fields
        game = request.data.get('game_id', None)
        game_inst = Game.objects.get(pk=game)
        category = request.data.get('category_id', None)
        category_inst = Category.objects.get(pk=category)

        if game is None or category is None:
            return Response({'message': 'please provide both a game and category'}, status=status.HTTP_400_BAD_REQUEST) 

        #instantiate GamesCategory
        new_game_category = GameCategory()

        #save request values to new instance of gamecategory
        new_game_category.game = game_inst
        new_game_category.category = category_inst

        #save to db
        new_game_category.save()

        #serialize
        serialized_game_category = GameCategorySerializer(new_game_category)

        #return response
        return Response(serialized_game_category.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game_category = GameCategory.objects.get(pk=pk)
            game_category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except GameCategory.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        selected_game = request.query_params.get('game', None)

        if selected_game is not None:
            try:
                game = Game.objects.get(pk=selected_game)
            except Game.DoesNotExist:
                return Response({'message':'You have requested reviews for a game that does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            game_categories = GameCategory.objects.filter(game=game)
            serialized_game_categories = GameCategorySerializer(game_categories, many=True)
            return Response(serialized_game_categories.data, status=status.HTTP_200_OK)
            
        game_categories = GameCategory.objects.all()
        serialized_game_categories = GameCategorySerializer(game_categories, many=True)
        return Response(serialized_game_categories.data, status=status.HTTP_200_OK)
    

    def update(self, request, pk): 
        # extract fields from client request
        game = request.data.get('game_id', None)
        category = request.data.get('category_id', None)

        if game is None or category is None :
            return Response({'Message': 'You must include game and category in your request'}, status=status.HTTP_400_BAD_REQUEST)
        
        #instantiate an object from the specified row in db
        game_inst = Game.objects.get(pk=game)
        category_inst = Category.objects.get(pk=category)
        try:
            game_category_to_update = GameCategory.objects.get(pk=pk)
        #update columns with request data
            game_category_to_update.game = game_inst
            game_category_to_update.category = category_inst
        #save new row
            game_category_to_update.save()
        #return success with no response body
            return Response({"message": "game successfully updated"}, status=status.HTTP_204_NO_CONTENT)
        
        except GameCategory.DoesNotExist:
                return Response({'Response': 'The game category you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)


class GameCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GameCategory
        fields = ['id', 'game', 'category']