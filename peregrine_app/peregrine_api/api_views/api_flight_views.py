from rest_framework.response import Response
from rest_framework.decorators import api_view
from peregrine_app.peregrine_api.api_serializers.flight_serializer import FlightSerializer
from django.http import JsonResponse
from peregrine_app.models import Flight
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from peregrine_app.facades.airlinefacade import AirlineFacade

anonymousfacade = AnonymousFacade()
airlinefacade = AirlineFacade()




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def flight_list(request, id=None):



    # GET REQUESTS
    if request.method == 'GET':
        if 'origin' in request.query_params:
            # Handle 'get_flights_by_origin_country' for all users
            origin_country = request.query_params['origin']
            flights = anonymousfacade.get_flights_by_origin_country_id(origin_country_id=origin_country)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'destination' in request.query_params:
            # Handle 'get_flights_by_destination_country' for all users
            destination_country = request.query_params['destination']
            flights = anonymousfacade.get_flights_by_destination_country_id(destination_country_id=destination_country)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'airline' in request.query_params:
            # Handle 'get_my_flights_by_airline_company' for airline users
            airline_company = request.query_params['airline']
            flights = anonymousfacade.get_flights_by_airline_company(airline_company_id=airline_company)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'departure' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            departure_time = request.query_params['departure']
            flights = anonymousfacade.get_flights_by_departure_date(departure_time=departure_time)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)           
        
        elif 'landing' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            landing_time = request.query_params['landing']
            flights = anonymousfacade.get_flights_by_landing_date(landing_time=landing_time)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)           
        else:
            # Handle 'get_all_flights' for other users
            flights = anonymousfacade.get_all_flights()
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
    
    
    #POST REQUESTS
    elif request.method == 'POST':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            # Use validated data instead of request.data
            new_flight = airlinefacade.add_flight(data=serializer.validated_data, airlinecompany=airlinecompany)
            if new_flight == False:
                return Response("Airline is allowed to add flights with its Id ONLY", status=status.HTTP_403_FORBIDDEN)
            if new_flight == 1:
                return Response("Invalid Country Id", status=status.HTTP_400_BAD_REQUEST)
            serializer = FlightSerializer(new_flight)
            return Response({"message": "Flight Created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # PUT REQUESTS
    elif request.method == 'PUT':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)                
        airlinecompany = request.user.airlinecompany
        flight = airlinefacade.get_flight_by_id(id=id)
        if flight is None:
            return Response("Flight not found", status=status.HTTP_404_NOT_FOUND)
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            if airlinefacade.update_flight(data=serializer.validated_data, flight_id=id, airlinecompany=airlinecompany) == False:
                return Response("Airline is allowed to update flights with its Id ONLY", status=status.HTTP_403_FORBIDDEN)  
            return Response({"message": "Flight updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE REQUESTS
    elif request.method == 'DELETE':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())) :
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany  
        remove_flight = airlinefacade.remove_flight(flight_id=id,airlinecompany=airlinecompany)
        if remove_flight == 0:
            return Response("Flight not found", status=status.HTTP_404_NOT_FOUND)               
        if remove_flight == 1:
            return Response("Cannot Remove Another Airline's Flight !", status=status.HTTP_403_FORBIDDEN)
        elif remove_flight ==2:
            return Response("This flight has an on going active/pruchased tickets thus cannot be removed !", status=status.HTTP_403_FORBIDDEN)
        return Response("Flight removed succesfully",  status=status.HTTP_202_ACCEPTED)







