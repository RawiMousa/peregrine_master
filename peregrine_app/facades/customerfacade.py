"""CustomerFacade is the customer's "app" or we can call it permissions.
It inherits the generic get functions from FacadeBase. Initializing its constructor,
requests the permitted dals from the Father class (Facadebase) """

# Importing the needed Facade and the needed utilities
from .facadebase import FacadeBase
from django.db import transaction

 # Custom made error, which handles the case, 
 # of a function requesting a DAL or a function which are not initialized in the constructor
from peregrine_app.exceptions import AccessDeniedError   


class CustomerFacade(FacadeBase):

    def __init__(self):
        super().__init__(dals=['customer_dal', 'ticket_dal'])
    
    @property
    def accessible_dals(self):
        return [('customer_dal', ['update_customer','get_customer_by_id']), ('ticket_dal', ['add_ticket', 'remove_ticket', 'get_ticket_by_id','get_tickets_by_customer_id']),('user_dal', ['update_user'])]
    
    
    def get_customer_by_id(self, customer_id):
        if self.check_access('customer_dal', 'get_customer_by_id'):
            try:
                return self.customer_dal.get_customer_by_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while updating customer: {e}")
                return None
        else:
            raise AccessDeniedError
            
    # def update_customer(self, customer_id, data):
    #     if self.check_access('customer_dal', 'update_customer'):
    #         try:
    #             return self.customer_dal.update_customer(customer_id=customer_id, data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating customer: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError

    def add_ticket(self, data):
        if (self.check_access('ticket_dal', 'add_ticket')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) :
            with transaction.atomic():
                try:
                    tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=(data['customer_id']))
                    flight = data['flight_id']
                    for ticket in tickets:
                        if ticket.flight_id == flight:
                            return False
                    if flight.remaining_tickets == 0:
                        print('The selected flight has no available tickets. In case of canecllation please check later')
                        return None
                    flight.remaining_tickets = (flight.remaining_tickets) - 1
                    flight.save()
                    self.ticket_dal.add_ticket(data=data)
                    return True
                except Exception as e:
                    transaction.set_rollback(True)
                    print(f"An error occurred while purchasing ticket: {e}")
                    return None
        else:
            raise AccessDeniedError

    def remove_ticket(self, id):
        if (self.check_access('ticket_dal', 'remove_ticket')) and (self.check_access('ticket_dal', 'get_ticket_by_id')):
            with transaction.atomic():             
                try:
                    ticket = self.ticket_dal.get_ticket_by_id(id=id)
                    flight = ticket.flight_id
                    flight.remaining_tickets = (flight.remaining_tickets) + 1
                    flight.save()
                    self.ticket_dal.remove_ticket(id=id)
                    return True
                except Exception as e:
                    print(f"An error occurred while removing ticket: {e}")
                    return None
        else:
            raise AccessDeniedError

    def get_my_tickets(self, customer_id):
        if self.check_access('ticket_dal', 'get_ticket_by_id'):
            try:
                return self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while fetching tickets: {e}")
                return None
        else:
            raise AccessDeniedError
        
    # def update_user(self,id, data):
    #     if self.check_access('user_dal', 'update_user'):
    #         try:
    #             return self.user_dal.update_user(id=id,data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating customer: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
        


    def update_customer(self,customer_id,user_id, user_data, data):
        if (self.check_access('customer_dal','update_customer')) and (self.check_access('user_dal','update_user')) :
            customer = self.customer_dal.get_customer_by_id(customer_id=customer_id)
            if (customer is None) or (not customer.exists()) :
                return 4
            try:
                with transaction.atomic():  
                    update_user = self.user_dal.update_user(id=user_id,data=user_data)
                    update_customer = self.customer_dal.update_customer(customer_id=customer_id,data=data)
                    return update_user, update_customer
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding a customer: {e}")
                return None
        else:
            raise AccessDeniedError