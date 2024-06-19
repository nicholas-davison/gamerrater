from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game
from django.contrib.auth.models import User

class ReviewViewSet(ViewSet):

    def create(self, request):
        review = Review()
        review.game = Game.objects.get(pk=request.data["game_id"])
        review.user = request.auth.user
        review.comment = request.data["comment"]

        try:
            review.save()
            serializer = ReviewSerializer(review, many=False)
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

            reviews = Review.objects.filter(game=game)
            serialized_reviews = ReviewSerializer(reviews, many=True)
            return Response(serialized_reviews.data, status=status.HTTP_200_OK)
            
        reviews = Review.objects.all()
        serialized_reviews = ReviewSerializer(reviews, many=True)
        return Response(serialized_reviews.data, status=status.HTTP_200_OK)

        

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields =('id', 'game', 'user', 'comment' )