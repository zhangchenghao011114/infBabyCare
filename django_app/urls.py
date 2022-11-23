from django.contrib import admin
from django.urls import path,include 
from django.views.static import serve
from backlogic import views
from HeadNurseBackstage import views as headnurse_views
import os

urlpatterns = [
    #path('admin/', admin.site.urls),
    # path('img/',)
    path('',headnurse_views.logpage),                # 登录页
    path('registerpage',headnurse_views.registerpage),                # 注册页
    path('admin/',admin.site.urls),
    path('mainpage',headnurse_views.mainpage),       # 主页
    path('nursemanagementpage',headnurse_views.nursemanagementpage),       # 护士管理页面
    path('inspectionpage',headnurse_views.inspectionpage),       # 巡查记录页面
    path('hazardpage',headnurse_views.hazardpage),       # 巡查记录页面
    path('test',views.test.as_view()),
    path('login',views.login.as_view()),
    path('register',views.register.as_view()),
    path('img/<str:img_name>',views.img.as_view()),
    path('test/<str:html_file>',views.testhtml.as_view()),
    path('api/patient/<str:patient_id>',views.patientGroups.as_view()),
    path('api/nurse',views.nurseGroups.as_view()),
    path('api/infusion',views.infusionGroups.as_view()),
    path('api/hazard',views.hazardGroups.as_view()),
    path('api/inspection',views.inspectionGroups.as_view()),
    path('api/patient2nurse',views.patient2nurse.as_view()),
    # path('api/infusion/<str:nurse_id>/',views.infusionGroups.as_view()),
]
