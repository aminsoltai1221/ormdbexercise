from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    IntegerField,
    ForeignKeyField,
    fn,
)
import datetime

# 1. اتصال به پایگاه داده
DATABASE = SqliteDatabase('company_database.db')

# 2. تعریف مدل پایه
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
        eng_dept = Department.create(department_name='Engineering') # دپارتمان بزرگتر

        # **تغییر در اینجا: پاس دادن department.id به جای شیء department**
        Employee.create(employee_name='Alice', department=hr_dept.id)
        Employee.create(employee_name='Bob', department=hr_dept.id)

        Employee.create(employee_name='Charlie', department=it_dept.id)
        Employee.create(employee_name='David', department=it_dept.id)
        Employee.create(employee_name='Eve', department=it_dept.id)

        Employee.create(employee_name='Frank', department=sales_dept.id)

        # دپارتمان مهندسی با بیشترین کارمند (5 کارمند)
        Employee.create(employee_name='Grace', department=eng_dept.id)
        Employee.create(employee_name='Heidi', department=eng_dept.id)
        Employee.create(employee_name='Ivan', department=eng_dept.id)
        Employee.create(employee_name='Judy', department=eng_dept.id)
        Employee.create(employee_name='Kevin', department=eng_dept.id)
        print("داده‌های نمونه با موفقیت درج شدند.")

except Exception as e:
    print(f"خطا در تنظیم دیتابیس یا درج داده: {e}")

# 5. ساخت Subquery برای یافتن ID بزرگترین دپارتمان
try:
    with DATABASE:
        print("\n--- اجرای Query با Subquery ---")

        largest_department_id_subquery = (
            Employee.select(Employee.department)
            .group_by(Employee.department)
            .order_by(fn.COUNT(Employee.id).desc())
            .limit(1)
        )

        # 6. استفاده از Subquery در پرس و جوی اصلی
        employees_in_largest_department = (
            Employee.select(Employee.employee_name, Department.department_name)
            .join(Department) # برای دسترسی به نام دپارتمان
            .where(Employee.department == largest_department_id_subquery)
        )

        # 7. نمایش نتایج
        print(f"کارکنان در بزرگترین دپارتمان (تعداد: {employees_in_largest_department.count()}):")
        if employees_in_largest_department.count() == 0:
            print("هیچ کارمندی در بزرگترین دپارتمان یافت نشد.")
        else:
            for employee in employees_in_largest_department:
                print(f"- نام کارمند: {employee.employee_name}, دپارتمان: {employee.department.department_name}")
        print("--- پایان اجرای Query ---")

except Exception as e:
    print(f"خطا در اجرای Query یا Subquery: {e}")
finally:
    if not DATABASE.is_closed():
        DATABASE.close()
        print("اتصال پایگاه داده بسته شد.")
