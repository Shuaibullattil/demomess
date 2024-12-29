from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('register/', views.student_form, name = 'student_form'),
    path('login/', views.userLogin, name = 'user_Login'),
    path('profile/<int:user_id>/', views.user_profile, name = 'user_profile'),
    path('dashboard/<int:id>/',views.dashboard,name = 'dashboard'),
    path('messcut/<int:id>/',views.messcut,name = "messcut"),
    path('controlpanel/',views.openControlPanel,name = 'controlPanel'),
    path('messcutpanel/',views.openMessCutPanel,name = 'messCutPanel'),
    path('messbillpanel/',views.openMessBillPanel,name = 'messBillPanel'),
    path('applybill/<str:month>/',views.applyMonthlyBill,name = 'applyBill'),
    path('billing/',views.generateBill,name = 'billing'),
    path('panelmenu/',views.openAdminPanel,name = 'panelMenu'),
    path('panelmenu/remove/<int:id>/',views.removeUser,name = 'remove'),
      
]
