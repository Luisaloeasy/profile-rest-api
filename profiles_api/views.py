from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):

    def get(self, request, format=None):
        """Return  listo of APIView features"""
        an_apiview = [

                'Uses HTTP methods as function ',
                'Is similar to a traditional djando view',
                'Gives you the most control over your aplication logic',
                'Is mapped manually to URLs',
            
        ]
        return Response({'messages':'Hello!', 'an_apiview':an_apiview}) 