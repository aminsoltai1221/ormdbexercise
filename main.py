from itertools import product
from peewee import SqliteDatabase,IntegrityError,Database


from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, fn

# اتصال به پایگاه داده SQLite
db = SqliteDatabase('sales.db')

# تعریف مدل پایه
class BaseModel(Model):
    class Meta:
        database = db

# تعریف مدل Product
class Product(BaseModel):
    name = CharField()

# تعریف مدل Sales
class Sales(BaseModel):
    product = ForeignKeyField(Product, backref='sales')
    quantity = IntegerField()
    price = IntegerField()  # قیمت واحد محصول در هر فروش

# ایجاد جداول و اتصال به پایگاه داده
db.connect()
db.create_tables([Product, Sales], safe=True)


def populate_sample_data():
    if Product.select().count() == 0:
        # ایجاد چند محصول
        products = [
            {'name': 'loptop'},
            {'name': 'phone'},
            {'name': 'headphone'}
        ]
        Product.insert_many(products).execute()

        # افزودن داده‌های فروش
        sales_data = [
            {'product': 1, 'quantity': 2, 'price': 1000},  # لپ‌تاپ: 2 عدد، هر کدام 1000
            {'product': 1, 'quantity': 1, 'price': 1000},  # لپ‌تاپ: 1 عدد
            {'product': 2, 'quantity': 5, 'price': 500},   # موبایل: 5 عدد
            {'product': 2, 'quantity': 3, 'price': 500},   # موبایل: 3 عدد
            {'product': 3, 'quantity': 10, 'price': 50}    # هدفون: 10 عدد
        ]
        Sales.insert_many(sales_data).execute()
        
def calculate_total_sales():
    # کوئری با select، SUM و group_by
    query = (Sales
             .select(
                 Product.name,
                 fn.SUM(Sales.quantity * Sales.price).alias('total_sales')
             )
             .join(Product)
             .group_by(Product.name))

    # نمایش نتایج
    print("مجموع فروش هر محصول:")
    for row in query:
        print(f"محصول: {row.product.name}, مجموع فروش: {row.total_sales}")

if __name__ == "__main__":
    # populate_sample_data()
    calculate_total_sales()
