from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'coleccion'

    def get(self, request):

        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}') # type: ignore
		    
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
	        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
	        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
	        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
    
class LandingAPIDetail(APIView):

    name = 'Landing Detail API'

    collection_name = 'coleccion'

    def get(self, request, pk):

        ref = db.reference(f'{self.collection_name}/{pk}')
        document = ref.get()

        if document:
            return Response(document, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Documento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        document = ref.get()

        if not document:
            return Response({"error": "404 Not Found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'email' not in data:
            return Response({"error": "Faltan campos requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        
        ref.update(data)

        return Response({"message": "Documento actualizado correctamente"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        document = ref.get()

        if document is not None:
            ref.delete()
            return Response({"message": "Documento eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Si no se encuentra el documento, retornamos error 404
            return Response({"error": "Documento no encontrado"}, status=status.HTTP_404_NOT_FOUND)