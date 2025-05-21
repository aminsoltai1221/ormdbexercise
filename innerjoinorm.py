# ایمپورت کردن کلاس ها و توابع مورد نیاز از peewee
from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    IntegerField,
    ForeignKeyField,
)
import datetime

# 1. اتصال به پایگاه داده
# نام فایل دیتابیس را اینجا تعیین کنید.
DATABASE = SqliteDatabase('company_database.db')

# 2. تعریف مدل پایه
# این مدل پایه به همه مدل‌های دیگر می‌گوید که از کدام دیتابیس استفاده کنند.
class BaseModel(Model):
    class Meta:
        database = DATABASE

# 3. تعریف مدل‌ها (Department و Employee)
class Department(BaseModel):
    department_name = TextField(unique=True)

    class Meta:
        table_name = 'departments'

class Employee(BaseModel):
    employee_name = TextField()
    # کلید خارجی به جدول departments
    department = ForeignKeyField(Department, backref='employees', on_delete='CASCADE')

    class Meta:
        table_name = 'employees'

# 4. ایجاد جدول‌ها و اضافه کردن داده‌ها
try:
    with DATABASE:
        print("اتصال به پایگاه داده برقرار شد.")

        # ایجاد جدول‌ها (اگر وجود ندارند)
        DATABASE.create_tables([Department, Employee])
        print("جداول Department و Employee ایجاد شدند (اگر قبلاً وجود نداشتند).")

        # حذف داده‌های قبلی برای شروع تازه در هر اجرا
        Employee.delete().execute()
        Department.delete().execute()

        print("\nدرج داده‌های نمونه...")
        # ایجاد دپارتمان‌ها و ذخیره ID آن‌ها
        hr_dept = Department.create(department_name='HR')
        it_dept = Department.create(department_name='IT')
        sales_dept = Department.create(department_name='Sales')
        eng_dept = Department.create(department_name='Engineering')

        # ایجاد کارکنان با استفاده از department_id (همانطور که قبلاً درخواست شده بود)
        Employee.create(employee_name='Alice', department=hr_dept.id)
        Employee.create(employee_name='Bob', department=hr_dept.id)

        Employee.create(employee_name='Charlie', department=it_dept.id)
        Employee.create(employee_name='David', department=it_dept.id)
        Employee.create(employee_name='Eve', department=it_dept.id)

        Employee.create(employee_name='Frank', department=sales_dept.id)

        Employee.create(employee_name='Grace', department=eng_dept.id)
        Employee.create(employee_name='Heidi', department=eng_dept.id)
        Employee.create(employee_name='Ivan', department=eng_dept.id)
        Employee.create(employee_name='Judy', department=eng_dept.id)
        Employee.create(employee_name='Kevin', department=eng_dept.id)
        print("داده‌های نمونه با موفقیت درج شدند.")

except Exception as e:
    print(f"خطا در تنظیم دیتابیس یا درج داده: {e}")

# 5. انجام عملیات INNER JOIN در peewee
try:
    with DATABASE:
        print("\n--- بازیابی اسامی کارکنان و نام دپارتمان‌هایشان با JOIN ---")

        # کوئری برای انتخاب employee_name از Employee و department_name از Department
        # .join(Department) به صورت پیش‌فرض یک INNER JOIN بر روی ForeignKeyField مربوطه انجام می‌دهد.
        # در اینجا، Employee.department یک ForeignKey به Department است، بنابراین Peewee می‌داند چگونه جوین کند.
        employees_with_department_names = (
            Employee.select(Employee.employee_name, Department.department_name)
            .join(Department) # جوین Employee با Department
        )

        # 6. نمایش نتایج
        if employees_with_department_names.count() == 0:
            print("هیچ کارمندی یافت نشد.")
        else:
            for employee in employees_with_department_names:
                # به employee.department.department_name دسترسی پیدا می‌کنیم.
                # Peewee شیء Department مرتبط را در ویژگی 'department' از شیء Employee قرار می‌دهد.
                print(f"کارمند: {employee.employee_name}, دپارتمان: {employee.department.department_name}")
        print("--- پایان نمایش نتایج ---")

except Exception as e:
    print(f"خطا در اجرای JOIN Query: {e}")
finally:
    if not DATABASE.is_closed():
        DATABASE.close()
        print("اتصال پایگاه داده بسته شد.")
