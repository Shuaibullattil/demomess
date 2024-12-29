from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Student,MessCut,MessBill,StudentBill
from datetime import datetime,timedelta
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from django.dispatch import receiver
from django.db.models.signals import post_save




# Create your views here.
def user_profile(request,user_id):
    return render(request,'user_profile.html',{'user' : Student.objects.get(id = user_id)})

def userRegister(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = UserCreationForm()    
    return render(request,'register.html',{'form' : form})



def student_form(request):
    if request.method == 'POST':
        # Extract form data
        mess_no = request.POST.get('mess_no', '')
        name = request.POST.get('name')
        dep = request.POST.get('dep')
        claim = request.POST.get('claim')
        food_pref = request.POST.get('food_pref')
        photo = request.FILES.get('photo')  # For file upload

        # Validate data (basic validation)
        errors = []
        if not mess_no or not name or not dep or not claim or not food_pref:
            errors.append("All fields are required.")
        if claim.lower() not in ['yes', 'no']:
            errors.append("Claim must be 'Yes' or 'No'.")

        # If errors, return to form with errors
        if errors:
            return render(request, 'createaccount.html', {'errors': errors})

        # Save the data
        Student.objects.create(
            mess_no=mess_no,
            name=name,
            dep=dep,
            claim=claim,
            food_pref=food_pref,
            photo=photo
        )
        # Redirect to the index page after saving
        return redirect('index')  # This will redirect to the URL pattern named 'index'
    
    else:
        return render(request, "createaccount.html")

# Automatically create a mess cut record when a new student is added
@receiver(post_save, sender=Student)
def create_messcut_for_new_student(sender, instance, created, **kwargs):
    if created:
        # Create a mess cut record for the new student
        MessCut.objects.create(
            student=instance,  # Link the MessCut record to the Student
            mess_no=instance.mess_no,
            student_name=instance.name
        )
        # Create a MessBill record
        StudentBill.objects.create(
            student=instance,
            mess_no=instance.mess_no,
            student_name=instance.name
        )
       



def index(request):
    if request.method == 'POST':
        temp_user_messno = request.POST.get('messNo')
        
        try:
            # Get the user with the specified mess_no
            user = Student.objects.get(mess_no=temp_user_messno)
            # Redirect to the user's profile page using the found user's ID
            return redirect(f'profile/{user.id}',{'user' : user })
        
        except Student.DoesNotExist:
            # If no user is found, return a response indicating so
            return HttpResponse("No user found with the specified mess number.", status=404)
    
    else:
        # Render the index page for non-POST requests
        return render(request, 'index.html')
    

def userLogin(request):
    if request.method == "post":
        form = AuthenticationForm(data  = request.POST)
        if form.is_valid():
            login(request,form.get.user())
            return redirect('login')
    form = AuthenticationForm()
    return render(request,'login.html',{'form' : form})     
    

def dashboard(request,id):
    user = Student.objects.get(id = id)
    mess_no = user.mess_no
    fee_detail = StudentBill.objects.get(mess_no = mess_no)
    return render(request,'dashboard.html',{'data' : fee_detail, 'user' : user})



def messcut(request, id):
    user = get_object_or_404(Student, id=id)
    
    messcutdays = 0
    error_message = ""

    # Get today's date and the current month's range
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(day=31)
    else:
        end_of_month = (start_of_month.replace(month=today.month + 1) - timedelta(days=1))

    
    # Fetch the MessCut record for the user
    

    if request.method == 'POST':
        fDate = request.POST.get('fromdate')
        tDate = request.POST.get('todate')

        try:
            from_date = datetime.strptime(fDate, "%Y-%m-%d").date()
            to_date = datetime.strptime(tDate, "%Y-%m-%d").date()

            # Backend validations for dates
            if from_date < today:
                error_message = "'From Date' cannot be in the past."
            elif to_date < from_date:
                error_message = "'To Date' cannot be before 'From Date'."
            elif from_date < start_of_month or from_date > end_of_month:
                error_message = "'From Date' must be within the current month."
            elif to_date < start_of_month or to_date > end_of_month:
                error_message = "'To Date' must be within the current month."
            else:
                # Calculate days if dates are valid
                messcutdays = (to_date - from_date).days  + 1

                try:
                    mess_cut_record = MessCut.objects.get(student=user)
                except MessCut.DoesNotExist:
                    mess_cut_record = None

                # Initialize currentMonthCut to 0 (assuming absence if no data)
                current_month = today.month
                currentMonthCut = 0

                if current_month == 1:
                        mess_cut_record.january += messcutdays
                elif current_month == 2:
                    mess_cut_record.february += messcutdays
                elif current_month == 3:
                    mess_cut_record.march += messcutdays
                elif current_month == 4:
                    mess_cut_record.april += messcutdays
                elif current_month == 5:
                    mess_cut_record.may += messcutdays
                elif current_month == 6:
                    mess_cut_record.june += messcutdays
                elif current_month == 7:
                    mess_cut_record.july += messcutdays
                elif current_month == 8:
                    mess_cut_record.august += messcutdays
                elif current_month == 9:
                    mess_cut_record.september += messcutdays
                elif current_month == 10:
                    mess_cut_record.october += messcutdays
                elif current_month == 11:
                    mess_cut_record.november += messcutdays
                elif current_month == 12:
                    mess_cut_record.december += messcutdays
                    
                    # Save the updated record
                mess_cut_record.save()


        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD format."

    return render(request, 'messcut.html', {
        'user': user,
        'messcutdays': messcutdays,
        'error_message': error_message,
        'today': today,
        'end_of_month': end_of_month
    })


def openAdminPanel(request):
    students = Student.objects.all()
    return render(request,'adminwindow.html',{'data' : students})

def openMessCutPanel(request):
    students = MessCut.objects.all()
    return render(request,'messcutpanel.html',{'users' : students})

def openMessBillPanel(request):
    students = StudentBill.objects.all()
    return render(request,'messbillpanel.html',{'users' : students})



def generateBill(request):
    students = MessBill.objects.all()
    if request.method == 'POST':
        # Extract data from the form
        month = request.POST.get('month')
        effective_days = request.POST.get('effectiveDays')
        cost_per_day = request.POST.get('costPerDay')
        est_fee = request.POST.get('establishmentFee')

        # Basic validation (optional)
        if not month or not effective_days or not cost_per_day or not est_fee:
            error_message = "All fields are required."
            return render(request, 'billgenerate.html', {'error_message': error_message,'users' : students})
        
        # Convert numeric fields to integers
        try:
            effective_days = int(effective_days)
            cost_per_day = int(cost_per_day)
            est_fee = int(est_fee)
        except ValueError:
            error_message = "Invalid numeric input. Please check your entries."
            return render(request, 'billgenerate.html', {'error_message': error_message,'users' : students})

        # Save the data to the model
        MessBill.objects.create(
            month=month,
            effectiveDays=effective_days,
            costPerDay=cost_per_day,
            estFee=est_fee,
            totalFee = effective_days * cost_per_day + est_fee
        )

        # Redirect to a success page or another view
        return redirect('/billing')  # Replace 'bill_success' with the name of your success view

    # Render the form for GET requests
    return render(request, 'billgenerate.html',{'users' : students})

def applyMonthlyBill(request, month):
    # Fetch fee data for the given month
    feeData = MessBill.objects.get(month=month)
    totalbill = feeData.totalFee
    cost_per_day = feeData.costPerDay

    # Fetch all student bills
    student_bills = StudentBill.objects.all()

    for student_bill in student_bills:
        # Get the related Student instance from the StudentBill instance
        student = student_bill.student  # Assuming a OneToOneField relation exists

        try:
            # Fetch the MessCut record for the student
            messcut = MessCut.objects.get(student=student)
            cut = getattr(messcut, month.lower(), 0)  # Get the mess cut dynamically for the month
        except MessCut.DoesNotExist:
            cut = 0  # Default to 0 if no mess cut is found

        # Calculate the final bill after applying the mess cut
        finalBill = totalbill - cost_per_day * cut

        # Dynamically set the fee for the corresponding month on the student_bill instance
        setattr(student_bill, f"{month.lower()}_fee", finalBill)
        student_bill.save()  # Save the updated record for each student_bill

    return redirect('/billing')  # Redirect to the billing page




def removeUser(request,id):
    temp = Student.objects.get(id = id)
    temp.delete()
    return redirect('/panelmenu')

def openControlPanel(request):
    return render(request,'controlpanel.html')













