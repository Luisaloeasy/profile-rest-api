from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test APIView"""
    #Cada vez que haga un POST o PUT requset llama a la classe HelloSerializer y ve los fields que tiene
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return  lista of APIView features"""
        an_apiview = [

                'Uses HTTP methods as function GET,POST,PATCH,PUT,DELETE',
                'Is similar to a traditional djando view',
                'Gives you the most control over your aplication logic',
                'Is mapped manually to URLs',
            
        ]
        return Response({'message':'Hello!', 'an_apiview':an_apiview}) 
    
    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        
        #Verificacion que cumpla con la validacion de serializer
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(                
                serializer.errors, 
                #status es el estado del response 200 is OK, 400 BAD
                status=status.HTTP_400_BAD_REQUEST              
                 )

    def put(self, request, pk=None):
        """Update entire object"""
        return Response({'method':'PUT'})

    def path(self, request, pk=None):
        """Para hacer updates parciales"""
        return Response({'method':'PATCH'})

    def delete(self,request, pk=None):
        """Eliminar objetos"""
        return Response({'method':'DELETE'})



class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
                'Uses action (list,create,retrieve,update,partial_update) ',
                'Automatically maps to URLs using Routers',
                'Provides more funcionality with less code ',        
        ]

        return Response({'message':'Hello!', 'a_viewset':a_viewset}) 

    def create(self,request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message= f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})
    
    def update(self,request,pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Update part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request,pk=None):
        """Delete an object"""
        return Response ({'http_method':'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profles """
    serializer_class= serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)




class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES




class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profiles feed item"""
    authentication_classes= (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes=(
        permissions.UpdateOwnStatus,IsAuthenticated)


    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)