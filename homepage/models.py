from django.db import models


# Create your models here.
class Student(models.Model):
    mess_no = models.IntegerField()
    name = models.CharField(max_length=30)
    dep = models.CharField(max_length=30)
    claim = models.CharField(max_length=3)
    food_pref = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='studimg')

    def __str__(self):
        return self.name


class MessCut(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the Student model
    mess_no = models.IntegerField()
    student_name = models.CharField(max_length=30)
    
    # Month fields for marking attendance (or mess cuts)
    january = models.IntegerField(default=0)  # 0 means absence, 1 means presence
    february = models.IntegerField(default=0)
    march = models.IntegerField(default=0)
    april = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    june = models.IntegerField(default=0)
    july = models.IntegerField(default=0)
    august = models.IntegerField(default=0)
    september = models.IntegerField(default=0)
    october = models.IntegerField(default=0)
    november = models.IntegerField(default=0)
    december = models.IntegerField(default=0)

    def __str__(self):
        return f"Mess Cut record for {self.student_name} (Mess No: {self.mess_no})"
    
class MessBill(models.Model):
    month = models.CharField(max_length=15)
    effectiveDays = models.IntegerField()
    costPerDay = models.IntegerField()
    estFee = models.IntegerField()
    totalFee = models.IntegerField(default=0)

    def __str__(self):
        return self.month
    
class StudentBill(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)  # Link to the Student model
    mess_no = models.IntegerField()
    student_name = models.CharField(max_length=30)
    
    # Monthly fee fields
    january_fee = models.IntegerField(default=0)
    february_fee = models.IntegerField(default=0)
    march_fee = models.IntegerField(default=0)
    april_fee = models.IntegerField(default=0)
    may_fee = models.IntegerField(default=0)
    june_fee = models.IntegerField(default=0)
    july_fee = models.IntegerField(default=0)
    august_fee = models.IntegerField(default=0)
    september_fee = models.IntegerField(default=0)
    october_fee = models.IntegerField(default=0)
    november_fee = models.IntegerField(default=0)
    december_fee = models.IntegerField(default=0)

    def __str__(self):
        return f"Mess Bill for {self.student_name} (Mess No: {self.mess_no})"
    


