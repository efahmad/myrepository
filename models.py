
class Product(models.Model):

    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __init__(self):
        self.inventory = 0

    def increase_inventory(self, amount):
        pass

    def decrease_inventory(self, amount):
        pass


class Customer(models.Model):

    user = models.OneToOneField(User,on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __init__(self):
        balance = 20000     # بیست هزار تومان اعتبار هدیه به محض تعریف در سامانه

    def deposit(self, amount):
        pass

    def spend(self, amount):
        pass


class OrderRow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.IntegerField()


class Order(models.Model):
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4

    status_choices = (
        (STATUS_SHOPPING, "در حال خرید"),
        (STATUS_SUBMITTED, "ثبت‌شده"),
        (STATUS_CANCELED, "لغوشده"),
        (STATUS_SENT, "ارسال‌شده"),
    )
    status = models.IntegerField(choices=status_choices)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_time = models.DateTimeField()
    total_price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    rows = models.ForeignKey(OrderRow, on_delete=models.PROTECT())   #در صورت سوال به صورت لیست است



    @staticmethod
    def initiate(customer):
        pass

    def add_product(self, product, amount):
        pass

    def remove_product(self, product, amount=None):
        pass

    def submit(self):
        pass

    def cancel(self):
        pass

    def send(self):
        pass


class User(models.Model):

    username = models.TextField()
    password = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()