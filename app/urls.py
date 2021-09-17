#from app.forms import CustomerRegistrationForm
from django.urls import path
from app import views
from django.conf import settings #for images
from django.conf.urls.static import static #for images
from django.contrib.auth import views as auth_views
from .forms import LoginForm ,MyPasswordChangeForm ,MyPasswordResetForm,MySetPasswordForm
from django.views.static import serve
from django.conf.urls import url
from .views import redirect_view
urlpatterns = [
    

    path('', views.ProductView.as_view(),name="index"),
    #  path('home/', views.ProductView.as_view(),name="home"),
    
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart,name="pluscart"),
    path('minuscart/',views.minus_cart,name="minuscart"),
    path('removecart/',views.remove_cart,name="minuscart"),
    path('removeadd/<int:pk>',views.remove_add,name="removeadd"),
    # path('otp',otp,name="otp"),
            


    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('payment/', views.payment, name='payment'),
    path('table/', views.table, name='table'),
    path('chair/',views.chair,name='chair'),
    path('sofa/', views.sofa, name='sofa'),
    # path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name="login"),
    path('customerregistration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    
    path('login/', redirect_view),
    path('logout/',auth_views.LogoutView.as_view(next_page='index'),name='logout'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm ,success_url="/passwordchangedone/"),name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
     url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    # ... more URL patterns here

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)