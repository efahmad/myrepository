## JUST for testing version 2

class Product(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()  # ولیدیتور رو نذار
    inventory = models.PositiveIntegerField(default=0)   #validators=[MinValueValidator(0)]

    # def __init__(self):
    #     self.inventory = 0

    def increase_inventory(self, amount):
        self.inventory+=amount
        self.save()     # برای ذخیره تغییرات

    def decrease_inventory(self, amount):
        if (self.inventory >= amount):
            self.inventory-=amount
            self.save()
        else:
            raise Exception('مقدار درخواست شده جهت حذف از سبد، بیش از مقدار موجودی است')

class User(models.Model):
    username = models.CharField()
    password = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.PositiveIntegerField(default=20000)

    # def __init__(self):
    #     balance = 20000     # بیست هزار تومان اعتبار هدیه به محض تعریف در سامانه

    def deposit(self, amount):      # شارژ حساب
        self.balance+=amount
        self.save()

    def spend(self, amount):    # خرج کردن
        if (self.balance>=amount):
            self.balance-=amount
            self.save()
        else:
            raise Exception('کمبود اعتبار: مبلغ درخواست شده، بیش از اعتبار موجود می باشد. لطفا ابتدا حساب خود را شارژ نموده و مجددا تلاش نمایید.')



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
    status = models.IntegerField(choices=status_choices) #, default=STATUS_SHOPPING

    customer = models.ForeignKey(null=True ,blank=True ,Customer, on_delete=models.PROTECT)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField()
    # rows = models.ForeignKey(OrderRow, on_delete=models.PROTECT())   #در صورت سوال به صورت لیست است


    @staticmethod
    def initiate(customer):
        o = Order()
        o.status = Order.STATUS_SHOPPING    # وضعیت در حال خرید
        o.customer = customer
        o.save()

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

class OrderRow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()