from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('team', views.team, name='team'),
    path('blog', views.blog, name='blog'),
    
    # Authentication
    path('register', views.register, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    
    # Password reset
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), 
         name="reset_password"),
    
    # Quizzes
    path('main', views.main_view, name='main-view'),
    path('<int:pk>/', views.quiz_view, name='quiz-view'),
    path('<int:pk>/data', views.quiz_data_view, name='quiz-data-view'),
    path('<int:pk>/save/', views.save_quiz_view, name='save-view'),
    
    # Add Quiz, Question, Answer, see Results
    path('upload_csv', views.upload_csv, name='upload-csv'), 
    path('results', views.results, name="results-view" ),
     
]
