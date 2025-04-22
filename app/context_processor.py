from .models import Customer

def customer_name(request):
    # print("Customer context processor called...")  # 👈 just to test
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            print(f"Found customer: {customer.name}")
            return {'customer_name': customer.name}
    return {'customer_name': None}

