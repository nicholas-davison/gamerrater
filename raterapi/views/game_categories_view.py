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


class GameCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GameCategory
        fields = ['id', 'game', 'category']