## JUST for testing version 3

class Product(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
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
        if Order.objects.filter(customer=customer, status=Order.STATUS_SHOPPING).exist():
            raise Exception("There is already a shopping order for this customer in the db.") 
        o = Order()
        o.status = Order.STATUS_SHOPPING    # وضعیت در حال خرید
        o.customer = customer
        o.save()
        return o

    def add_product(self, product, amount):
        if (amount == 0): #امکان افزودن صفر عدد از یک کالا به سبد خرید مشتری وجود ندارد.
            raise Exception('امکان افزودن صفر عدد از یک کالا به سبد خرید مشتری وجود ندارد.')
       # elif (product.inventory < amount):  #مشتری نمی‌تواند کالایی را بیش از ظرفیت موجود در فروشگاه به سبد خرید خود اضافه کند.
       #    raise Exception('کمبود کالا')
        else:
            
            self.total_price += product.price * amount
            self.save()
            # آیا باید inventory محصول را نیز همزمان از Product کم کنیم ؟

    def remove_product(self, product, amount=None):
        if (amount == None):        # اگر تعدادی مشخص نشده بود، کلا Object OrderRow را Delete کن.
            OrderRow.objects.filter(product__orderrow__order_id=product.id)[0].delete()
        elif OrderRow.objects.filter(product__orderrow__order_id=product.id).count()>0:   # اگر محصول وارد شده در تابع، در این سفارش موجود نبود :
            raise Exception('عدم وجود کالا جهت کم کردن از سبد خرید')
        else:
            self.total_price -= product.price*amount
            self.save()

    def submit(self):
        #در زمان ثبت سفارش، اولا باید بررسی شود که از تمام کالاهای مورد سفارش مشتری به اندازه کافی در فروشگاه وجود داشته باشد،
        # بحث چک کردن میزان موجودی، در تابع addproduct بررسی می شود.

        # ثانیا باید مشتری به اندازی جمع مبلغ سفارش خود اعتبار داشته باشد
        # یعنی این شرط برقرار باشد  self.total_price =<  اعتبار مشتری  customer.balance
        if self.total_price >= Customer.objects.get(id = self.customer_id ).balance :   # اگرکل مبلغ سفارش بیش از اعتبار مشتری بود
            self.status = self.STATUS_SHOPPING #در صورتی که ثبت سفارش با موفقیت انجام نشود، سفارش «در حال خرید» باقی می‌ماند و موجودی کالاها و اعتبار مشتری نیز دست نمی‌خورد.
            self.save()
            raise Exception('کمبود اعتبار')
        else:
            self.status = self.STATUS_SUBMITTED  # سفارش «ثبت‌شده» تلقی می‌شود و پول آن از حساب مشتری کاسته شده و موجودی کالاها نیز از موجودی فروشگاه کم می‌شوند.
            self.save()
            c = Customer.objects.get(id = self.customer_id )    # ول آن از حساب مشتری کاسته شده
            c.balance -= self.total_price
            c.save()

    def cancel(self):       # از سفارش خود انصراف داده و اعتبار خود را پس بگیرد. در این صورت وضعیت سفارش به «لغوشده» تغییر کرده و کالاها نیز به موجودی فروشگاه برمی‌گردند.
        pass
        # self.status = self.STATUS_CANCELED
        # self.save()

    def send(self):
        pass

class OrderRow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
