from src.repositories.order_repository import OrderRepository
from src.utils.exceptions import ValidationError

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
    
    def get_all_orders(self):
        return self.order_repository.get_all()
    
    def create_order(self, order_data):
        # Validate order data
        if not order_data.get('items'):
            raise ValidationError('Order must have at least one item')
            
        # Calculate total amount
        total_amount = sum(item['price'] * item['quantity'] for item in order_data['items'])
        order_data['total_amount'] = total_amount
        
        # Create order
        return self.order_repository.create(order_data)
