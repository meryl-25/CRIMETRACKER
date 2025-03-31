from django.urls import path
from ctapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path("",views.index,name="index"),
path("index",views.index,name="index"),
path("user_login",views.user_login,name="user_login"),
# path("user_registration",views.user_registration,name="user_registration"),
path('user_action', views.user_action,name="user_action"),
path("login_action",views.login_action,name="login_action"),
path('admin_logout', views.admin_logout,name="admin_logout"),
path('user_logout',views.user_logout,name="user_logout"),
path("user_registration",views.user_registration,name="user_registration"),
path('admin_home',views.admin_home,name="admin_home"),
path('user_home',views.user_home,name="user_home"),

path('add_category', views.add_category,name="add_category"),
path('save_category', views.save_category,name="save_category"),
path('edit_category/<int:id>', views.edit_category,name="edit_category"),
path('update_category/<int:id>', views.update_category,name="update_category"),
path('delete_category/<int:id>', views.delete_category,name="delete_category"),


path('users_list', views.users_list,name="users_list"),
path('profile', views.profile,name="profile"),



path('add_police_station',views.add_police_station,name="add_police_station"),
path('save_station',views.save_station,name="save_station"),
path('display_district',views.display_district,name="display_district"),   
path('list_police_station',views.list_police_station,name="list_police_station"),   
path('edit_police_station/<int:id>', views.edit_police_station,name="edit_police_station"),
path('update_police_station/<int:id>', views.update_police_station,name="update_police_station"),
path('delete_police_station/<int:id>', views.delete_police_station,name="delete_police_station"),

path('add_complaints', views.add_complaints,name="add_complaints"),
path('submit_complaint', views.submit_complaint,name="submit_complaint"),
path('display_police_station', views.display_police_station,name="display_police_station"),
path('view_complaints', views.view_complaints,name="view_complaints"),
path('crime_more/<int:id>', views.crime_more,name="crime_more"),
path('profile', views.profile,name="profile"),
path('view_feedback', views.view_feedback,name="view_feedback"),
path('feedback_replied_list', views.feedback_replied_list,name="feedback_replied_list"),
path('adm_reply_feedback/<int:id>', views.adm_reply_feedback,name="adm_reply_feedback"),
path('feedback', views.feedback,name="feedback"),
path('save_feedback', views.save_feedback,name="save_feedback"),
path('delete_feedback/<int:id>', views.delete_feedback,name="delete_feedback"),
path('add_reply_feedback/<int:id>', views.add_reply_feedback,name="add_reply_feedback"),


path('police_registration',views.police_registration,name="police_registration"),
path('save_police',views.save_police,name="save_police"),

path('submitted_police',views.submitted_police,name="submitted_police"),
path('approve_police/<int:id>',views.approve_police,name="approve_police"),
path('to_approve_police/<int:id>',views.to_approve_police,name="to_approve_police"),
path('reject_police/<int:id>',views.reject_police,name="reject_police"),
path('approved_list',views.approved_list,name="approved_list"),

path('search_police',views.search_police,name="search_police"),


path('submitted_crimes',views.submitted_crimes,name="submitted_crimes"),
path('assign_crimes/<int:id>',views.assign_crimes,name="assign_crimes"),
path('to_assign_crimes/<int:id>',views.to_assign_crimes,name="to_assign_crimes"),
path('assigned_crimes',views.assigned_crimes,name="assigned_crimes"),

path('adm_crime_more/<int:id>',views.adm_crime_more,name="adm_crime_more"),

path('display_police',views.display_police,name="display_police"),

path('transfer',views.transfer,name="transfer"),
path('transfer_details',views.transfer_details,name="transfer_details"),
path('save_transfer',views.save_transfer,name="save_transfer"),

path('p_assigned_crimes',views.p_assigned_crimes,name="p_assigned_crimes"),
path('police_home',views.police_home,name="police_home"),

path('crime_updates/<int:id>',views.crime_updates,name="crime_updates"),
path('save_updates/<int:id>',views.save_updates,name="save_updates"),

path('p_crime_more/<int:id>',views.p_crime_more,name="p_crime_more"),

path('adm_updates/<int:id>',views.adm_updates,name="adm_updates"),

path('district_wise',views.district_wise,name="district_wise"),

path('place_wise',views.place_wise,name="place_wise"),

path('adm_google_map_view_spot/<str:latitude>/<str:longitude>/', views.adm_google_map_view_spot, name='adm_google_map_view_spot'),

path('p_google_map_view_spot/<str:latitude>/<str:longitude>/', views.p_google_map_view_spot, name='p_google_map_view_spot'),

path('save_fir/<int:id>',views.save_fir,name="save_fir"),
path('add_fir/<int:id>',views.add_fir,name="add_fir"),
path('view_fir/<int:id>',views.view_fir,name="view_fir"),

path('p_profile',views.p_profile,name="p_profile"),


path('p_other_crimes',views.p_other_crimes,name="p_other_crimes"),
path('forget_password/', views.forget_password),

path('send_otp/', views.send_otp),
path('check_otp_action/', views.check_otp_action),
path('change_psd/', views.change_psd),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
