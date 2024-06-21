from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Rating
from django.contrib.auth.models import User

class RatingViewSet(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        rating = Rating()
        rating.user = request.auth.user
        rating.game = Game.objects.get(pk=request.data["game_id"])
        rating.rating = request.data.get('rating', None)

        if rating.rating is None:
            return Response({'message': 'you must submit a rating between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            rating.save()
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        selected_game = request.query_params.get('game', None)

        if selected_game is not None:
            try:
                game = Game.objects.get(pk=selected_game)
            except Game.DoesNotExist:
                return Response({'message':'You have requested reviews for a game that does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            rating = Rating.objects.filter(game=game)
            serialized_ratings = RatingSerializer(rating, many=True)
            return Response(serialized_ratings.data, status=status.HTTP_200_OK)
            
        ratings = Rating.objects.all()
        serialized_ratings = RatingSerializer(ratings, many=True)
        return Response(serialized_ratings.data, status=status.HTTP_200_OK)

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'game', 'rating',)