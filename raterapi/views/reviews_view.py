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
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields =('id', 'game', 'user', 'comment' )