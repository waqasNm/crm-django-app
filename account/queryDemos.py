# # *** (1) Returns all customers from customer table
# customers = Customers.objects.all()

# # *** (2) Returns first customer from customer table
# firstCustomer = Customers.objects.first()

# # *** (3) Returns last customer from customer table
# lastCustomer = Customers.objects.last()

# # *** (4) Returns single customer by name from customer table
# lastCustomer = Customers.objects.get(name='customer1')

# # *** (5) Returns single customer by id from customer table
# lastCustomer = Customers.objects.get(id=1)

# # *** (6) Returns all orders related to customer (firstCustomer variable set above)
# firstCustomer.order_set.all()

# # *** (7) Returns orders customer name: (Query parent model values)
# order = Order.objects.first()
# parentName = order.customer.name

# # *** (8) Returns products from the table with value of "Out Door" in category attribute
# products = Products.objects.filter(category="Out Door")

# # *** (9) Returns Order/Sort objects by id
# asc_order_products = Products.objects.all().order_by("id")
# desc_order_products = Products.objects.all().order_by("-id")


# # *** (10) Returns all products with tag of 'Sports': (Query Many to Many fields)
# productsFiltered = Product.objects.filter(tags__name="Sports")


