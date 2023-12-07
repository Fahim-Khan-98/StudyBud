from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def GetRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    context = {
        'routes': routes
    }

    return Response(context)


@api_view(['GET'])
def GetRooms(request):
    rooms = Room.objects.all()
    serilizer = RoomSerializer(rooms, many=True)
    return Response(serilizer.data)


def success_response(data):
    return Response(data, status=status.HTTP_200_OK)

def does_not_exist_response(pk):
    return Response({"message": f"No room available with ID {pk}"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def GetRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
        serializer = RoomSerializer(room, many=False)
        return success_response(serializer.data)
    except Room.DoesNotExist:
        return does_not_exist_response(pk)



# @api_view(['GET'])
# def GetRoom(request, pk):
#     try:
#         room = Room.objects.get(id=pk)
#         serializer = RoomSerializer(room, many=False)
#         return Response(serializer.data)
#     except Room.DoesNotExist:
#         return Response({"message": f"No room available with ID {pk}"}, status=status.HTTP_404_NOT_FOUND)
    