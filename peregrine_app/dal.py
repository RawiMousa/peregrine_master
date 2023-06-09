from .models import Country,Customer,Administrator,AirlineCompany,Flight,Ticket
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User , Group

class CountryDAL:

    @staticmethod
    def add_country(new_country):
        try:
            country = Country.objects.create(name=new_country)
            return country
        except Exception as e:
            print (f"An error occurred while adding the country: {e}")
            return None
    
    @staticmethod
    def get_all_countries():
        try:
            countries = Country.objects.values_list('name', flat=True)
            return countries
        except Country.DoesNotExist:
            print ('Country Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while showing countries: {e}")
            return None  
             
    @staticmethod
    def get_country_by_id(country_id):
        try:
            country = Country.objects.get(id=country_id)
            return country
        except Country.DoesNotExist:
            print ('Country Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while deleting country: {e}")
            return None
            
    @staticmethod
    def remove_country(country_id):
        try:
            country = Country.objects.get(id=country_id)
            country.delete()
        except Country.DoesNotExist:
            print ('Country Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while deleting country: {e}")
            return None


class CustomerDAL:

    @staticmethod
    def get_customer_by_id(customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            return customer
        except Customer.DoesNotExist:
            print ('Customer Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while deleting customer: {e}")
            return None
        
    @staticmethod
    def get_customer_by_username(username):
        try:
            customer = Customer.objects.filter(user_id__username=username)
            return customer
        except Customer.DoesNotExist:
            print ('Customer Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while deleting customer: {e}")
            return None
               
    @staticmethod
    def get_all_customers():
        try:
            all_customers = Customer.objects.all()
            return all_customers
        except Customer.DoesNotExist:
            print ('Customer Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while fetching customers: {e}")
            return None
        
    @staticmethod
    def add_customer(data):
        try:
            new_customer = Customer.objects.create(**data)
            return new_customer
        except Exception as e:
            print (f"An error occurred while adding customer: {e}")
            return None

    @staticmethod
    def update_customer(customer_id, data):
        try:
            update_customer = Customer.objects.filter(pk=customer_id).update(**data)
            return update_customer
        except Customer.DoesNotExist:
            print ('Customer Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while updating customer: {e}")
            return None
        
    @staticmethod
    def remove_customer(customer_id):
        try:
           customer =  Customer.objects.get(id=customer_id)
           customer.delete()
        except Customer.DoesNotExist:
            print ('Customer Does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occurred while removing customer: {e}")
            return None


class FlightDAL:

    @staticmethod
    def get_flights_by_origin_country_id(origin_country_id):
        try:
            flights = Flight.objects.filter(origin_country_id=origin_country_id)
            return flights
        except Flight.DoesNotExist:
            print ('Flights do not exist')
            return None
        except Exception as e:
            print (f"An error occurred while fetching flights: {e}")
            return None

    @staticmethod
    def get_flights_by_destination_country_id(destination_country_id):
        try:
            flights = Flight.objects.filter(destination_country_id=destination_country_id)
            return flights
        except Flight.DoesNotExist:
            print ('Flight does not exist')
            return None
        except Exception as e:
            print (f"An error occured while fetching flight : {e}")
            return None

    @staticmethod
    def get_flights_by_departure_date(departure_time):
        try:
            flights = Flight.objects.filter(departure_time=departure_time)
            return flights
        except Flight.DoesNotExist:
            print ('Flight does not exist')
            return None
        except Exception as e:
            print (f"An error occured while fetching flight : {e}")
            return None  

    @staticmethod
    def get_flights_by_landing_date(landing_time):
        try:
            flights = Flight.objects.filter(landing_time=landing_time)
            return flights
        except Flight.DoesNotExist:
            print ('Flight does not exist')
            return None
        except Exception as e:
            print (f"An error occured while fetching flight : {e}")
            return None 

    @staticmethod
    def get_flights_by_customer(customer_id):
        try:
            flights = Flight.objects.filter(ticket__customer_id=customer_id)
            return flights
        except Customer.DoesNotExist:
            print ('Customer does not exist in the DB')
            return None
        except Exception as e:
            print (f"An error occured while fetching flight : {e}")
            return None
                        
    @staticmethod
    def get_flights_by_airline_company_id(airline_company_id):
        try:
            flights = Flight.objects.filter(airline_company_id=airline_company_id)
            return flights
        except Flight.DoesNotExist:
            print ('flights do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching flights: {e}")
            return None

    @staticmethod
    def get_arrival_flights_by_country_id(country_id):
        current_time = timezone.now()
        twelve_hours_from_now = current_time + timezone.timedelta(hours=12)
        try:
            arrival_flights = Flight.objects.filter(
                Q(destination_country_id=country_id) & 
                Q(landing_time__gte=current_time, landing_time__lte=twelve_hours_from_now)
            )
            return arrival_flights
        except Flight.DoesNotExist:
            print ('flights do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching flights: {e}")
            return None
        
    @staticmethod
    def get_departure_flights_by_country_id(country_id):
        current_time = timezone.now()
        twelve_hours_from_now = current_time + timezone.timedelta(hours=12)
        try:
            arrival_flights = Flight.objects.filter(
                Q(origin_country_id=country_id) & 
                Q(departure_time__gte=current_time, departure_time__lte=twelve_hours_from_now)
            )
            return arrival_flights
        except Flight.DoesNotExist:
            print ('flights do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching flights: {e}")
            return None

    @staticmethod
    def get_flight_by_id(id):
        try:
            flight = Flight.objects.get(id=id)
            return flight
        except Flight.DoesNotExist:
            print ('Flight does not exist')
            return None
        except Exception as e:
            print (f"An error occured while fetching flight : {e}")
            return None
        
    @staticmethod
    def get_all_flights():
        try:
            all_flights = Flight.objects.all()
            return all_flights
        except Flight.DoesNotExist:
            print ('Flights do not exist')
            return None
        except Exception as e:
            print (f"An error occured while fetching flights : {e}")
            return None
        
    @staticmethod
    def add_flight(data):
        try:
            new_flight = Flight.objects.create(**data)
            return new_flight
        except Exception as e:
            print (f"An error occured while adding flight : {e}")
            return None
        
    @staticmethod
    def update_flight(flight_id,data):
        try:
            update_flight = Flight.objects.filter(id=flight_id).update(**data)
            return update_flight
        except Exception as e:
            print (f"An error occurred while updating flight: {e}")
            return None
       
    @staticmethod
    def remove_flight(flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
            flight.delete()
        except Flight.DoesNotExist:
            print ('Flight does not exist')
            return None
        except Exception as e:
            print (f"An error occurred while removing flight: {e}")
            return None


class AirlineCompanyDAL:

    @staticmethod
    def get_airline_company_by_id(id):
        try:
            airline_company = AirlineCompany.objects.get(id=id)
            return airline_company
        except AirlineCompany.DoesNotExist:
            print ('Airline company does not exist')
            return None
        except Exception as e:
            print (f"An error occurred while fetching airline company: {e}")
            return None
            
    @staticmethod
    def get_airline_by_username(username):
        try:
            airline_company = AirlineCompany.objects.filter(user_id__username=username)
            return airline_company
        except AirlineCompany.DoesNotExist:
            print ('Airline company does not exist')
            return None
        except Exception as e:
            print (f"An error occurred while fetching airline company: {e}")
            return None
     
    @staticmethod
    def get_all_airline_companies():
        try:
            companies = AirlineCompany.objects.all()
            return companies
        except AirlineCompany.DoesNotExist:
            print ('Airline companies do not exist')
            return None
        except Exception as e:
            print (f"An error occurred while fetching airline companies: {e}")
            return None
        
    @staticmethod
    def get_airlines_by_country(country_id):
        try:
            airline_companies = AirlineCompany.objects.filter(country_id=country_id)
            return airline_companies
        except AirlineCompany.DoesNotExist:
            print ('Airline companies do not exist')
            return None
        except Exception as e:
            print (f"An error occurred while fetching airline companies: {e}")
            return None
        
    @staticmethod
    def add_airline_company(data):
        try:
            new_airline_company = AirlineCompany.objects.create(**data)
            return new_airline_company
        except Exception as e:
            print (f"An error occurred while adding airline companies: {e}")
            return None
        
    @staticmethod
    def update_airline_company(id, data):
        try:
            airline_company = AirlineCompany.objects.filter(id=id).update(**data)
            return airline_company
        except AirlineCompany.DoesNotExist:
            print ('Airline company does not exist/is not found')
            return None
        except Exception as e:
            print (f"An error occurred while updating airline companies: {e}")
            return None
        
    @staticmethod
    def remove_airline_company(id):
        try:
            airline_company = AirlineCompany.objects.get(id=id)
            airline_company.delete()
        except AirlineCompany.DoesNotExist:
            print ('Airline company does not exist/is not found')
            return None
        except Exception as e:
            print (f"An error occurred while removing airline companies: {e}")
            return None


class AdministratorDAL:

    @staticmethod
    def get_admin_by_id(id):
        try:
            admin = Administrator.objects.get(id=id)
            return admin
        except Administrator.DoesNotExist:
            print ('Admin does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching admin: {e}")
            return None
        
    @staticmethod
    def get_all_admins():
        try:
            admins = Administrator.objects.all()
            return admins
        except Administrator.DoesNotExist:
            print ('Admins do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching admins: {e}")
            return None
        
    @staticmethod
    def add_new_admin(data):
        try:
            new_admin = Administrator.objects.create(**data)
            return new_admin
        except Exception as e:
            print (f"An error occurred while creating new admin: {e}")
            return None
        
    @staticmethod
    def update_admin(id, data):
        try:
            update_admin = Administrator.objects.filter(id=id).update(**data)
            return update_admin
        except Administrator.DoesNotExist:
            print ('Admin does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while updating admin: {e}")
            return None
        
    @staticmethod
    def remove_admin(id):
        try:
            admin = Administrator.objects.get(id=id)
            admin.delete()
        except Administrator.DoesNotExist:
            print ('Admin does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while deleting admin: {e}")
            return None          


class UserDAL:

    @staticmethod
    def get_user_by_id(id):
        try:
            user = User.objects.get(id=id)
            return user
        except User.DoesNotExist:
            print ('User does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching user: {e}")
            return None

    @staticmethod
    def get_user_by_username(username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            print ('User does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching user: {e}")
            return None       
           
    @staticmethod
    def get_all_users():
        try:
            users = User.objects.all()
            return users
        except User.DoesNotExist:
            print ('Users do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching users: {e}")
            return None

    @staticmethod
    def add_user(data):
        try:
            new_user = User.objects.create(
                username=data['username'],
                email=data['email']
            )
            new_user.set_password(data['password1'])
            new_user.save()
            return new_user
        except Exception as e:
            print (f"An error occurred while adding user: {e}")
            return None
        
    @staticmethod
    def update_user(id, data):
        try:
            user = User.objects.filter(id=id).update(**data)
            return user
        except User.DoesNotExist:
            print ('User does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while updating user: {e}")
            return None

    @staticmethod
    def remove_user(id):
        try:
            user = User.objects.get(id=id)
            user.delete()
        except User.DoesNotExist:
            print ('User does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while deleting user: {e}")
            return None
       
                     
class TicketDAL:

    @staticmethod
    def get_ticket_by_id(id):
        try:
            ticket = Ticket.objects.get(id=id)
            return ticket
        except Ticket.DoesNotExist:
            print ('ticket does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching ticket: {e}")
            return None

    @staticmethod
    def get_tickets_by_flight_id(flight_id):
        try:
            tickets = Ticket.objects.filter(flight_id=flight_id)
            return tickets
        except Ticket.DoesNotExist:
            print ('ticket/s does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching tickets: {e}")
            return None
               
    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        try:
            tickets = Ticket.objects.filter(customer_id=customer_id)
            return tickets
        except Ticket.DoesNotExist:
            print ('ticket/s does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching tickets: {e}")
            return None

    @staticmethod
    def get_all_tickets():
        try:
            tickets = Ticket.objects.all()
            return tickets
        except Ticket.DoesNotExist:
            print ('Tickets do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching tickets: {e}")
            return None 

    @staticmethod
    def add_ticket(data):
        try:
            new_ticket = Ticket.objects.create(**data) 
            return new_ticket
        except Exception as e:
            print (f"An error occurred while adding ticket: {e}")
            return None

    @staticmethod
    def update_ticket(id, data):
        try:
            updated = Ticket.objects.filter(id=id).update(**data)
            return updated
        except Ticket.DoesNotExist:
            print ('ticket does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while updatiing ticket: {e}")
            return None

    @staticmethod
    def remove_ticket(id):
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()
        except Ticket.DoesNotExist:
            print ('ticket does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while removing ticket: {e}")
            return None             
        

class GroupDAL:

    @staticmethod
    def get_userRole_by_role(user_role):
        try:
            user_role = Group.objects.get(name=user_role)
            return user_role
        except Group.DoesNotExist:
            print ('User role does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching user role: {e}")
            return None

    @staticmethod
    def get_all_userRoles():
        try:
            user_roles = Group.objects.all().values()
            return user_roles
        except Group.DoesNotExist:
            print ('User roles do not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while fetching user roles: {e}")
            return None
        
    @staticmethod
    def add_user_role(data):
        try:
            new_user_role = Group.objects.create(**data)
            return new_user_role
        except Exception as e:
            print (f"An error occurred while adding user role: {e}")
            return None   

    @staticmethod
    def update_user_role(id, data):
        try:
            user_role = Group.objects.filter(id=id).update(**data)
            return user_role
        except Group.DoesNotExist:
            print ('User role does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while updating user role: {e}")
            return None
        
    @staticmethod
    def remove_user_role(id):
        try:
            user = Group.objects.get(id=id)
            user.delete()
        except Group.DoesNotExist:
            print ('User role does not exist/not found')
            return None
        except Exception as e:
            print (f"An error occurred while deleting user role: {e}")
            return None


           
           

           
           


        


                
            
