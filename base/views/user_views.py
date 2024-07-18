from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from base.serializers import UserSerializer,UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # data['username']=self.user.username #user is default table
        # data['email']=self.user.email
        serializer=UserSerializerWithToken(self.user) #self.user refers to the authenticated user associated with the request.
        serializer=serializer.data
        for k,v in serializer.items():
            data[k]=v 
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    
    

# @api_view(['GET'])
# def getRoutes(request):
#     # return JsonResponse('Hello',safe=False) #When safe is True (which is the default):The data you pass to JsonResponse must be a dictionary. This is because JSON objects correspond to Python dictionaries.If you pass a non-dictionary object, a TypeError will be raised. so we kept safe=False
#     return Response('hello')



@api_view(['POST'])
def registerUser(request):
    data=request.data#The request.data attribute provides the parsed content of the request body
    try:
        user=User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer=UserSerializerWithToken(user,many=False) #retiurning only one user obj so many=false
        return Response(serializer.data)
    except:
        message={'detail':'user with this email already exists'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
        
        

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user=request.user #gives the loggin user details If the user is not authenticated (anonymous user), request.user typically returns an instance of AnonymousUser.
    serializer=UserSerializerWithToken  (user,many=False)
    data=request.data 


    user.first_name=data['name']
    user.username=data['email']
    user.email=data['email']
    if data['password']!='':
        user.password=make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user=request.user #gives the loggin user details If the user is not authenticated (anonymous user), request.user typically returns an instance of AnonymousUser.
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])

def deleteUser(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    return Response({'detail':'User deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    user=User.objects.get(id=pk)
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])

def updateUser(request,pk):
    data=request.data
    user=User.objects.get(id=pk)
    user.first_name=data['name']
    user.username=data['email']
    user.email=data['email']
    user.is_staff=data['isAdmin']
    user.save()
    serializer=UserSerializer(user,many=False)

    return Response(serializer.data)

    