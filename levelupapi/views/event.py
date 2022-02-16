
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer
from rest_framework.decorators import action

class EventView(ViewSet):
    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        gamer = Gamer.object.get(user=request.auth.user)
        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        event = Event.object.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.description = request.data['description']
        event.time = request.data['time']
        event.date = request.data['date']
        event.game = Game.objects.get(pk=request.data['game'])
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        gamer = Game.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)

        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True) # detail = true means expect pk false = events/leave true = events/pk/leave
    def leave(self, request, pk):
        gamer = Game.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)

        event.attendees.remove(gamer)
        return Response(status=status.HTTP_204_NO_CONTENT)



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('description', 'date', 'time', 'game')