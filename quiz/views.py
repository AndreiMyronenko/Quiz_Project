from django.shortcuts import render, redirect
from numpy import NaN
from .forms import CreateUserForm, QuizForm, CsvImportForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Quiz, Question, Answer, Result
from django.http import JsonResponse, HttpResponseRedirect
import pandas as pd


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def about(request):
    return render(request, 'about.html', {})


def team(request):
    return render(request, 'team.html', {})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"New account created: {user.username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("quiz:index")
        else:
            messages.error(request, "Account creation failed")
            
    form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect("quiz:index")
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('quiz:index')


def main_view(request):
    quiz = Quiz.objects.all()
    return render(request, 'main.html', {'obj': quiz})

    

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


def save_quiz_view(request, pk):
    if request.accepts('application/json'): 
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)
        
        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None
        
        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)
           
    return JsonResponse({'score': score_, 'results': results})


def add_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST, request.FILES)
        if quiz_form.is_valid():
            quiz_form.save()
            messages.success(request, "Your quiz was successfully added.")
        else:
            messages.error(request, "Error saving form")
            
        return redirect('quiz:index')
    quiz_form = QuizForm()
    quizzes = Quiz.objects.all()
    return render(request=request, template_name="add_quiz.html", context={'quiz_form': quiz_form, 'quizzes': quizzes})


def upload_csv(request):
    if request.method == "POST":    
        
        csv_file = request.FILES["csv_upload"]
        image = request.FILES["image"]
        
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, "The wrong file type was uploaded to the 'edited template' field.")
            return HttpResponseRedirect(request.path_info)
        
        df = pd.read_csv(csv_file, encoding='utf-8', encoding_errors='replace')
        
        if not image.name.endswith(('.jpg', '.png', '.gif')):
            messages.warning(request, "The wrong file type was uploaded to the 'image' field.")
            return HttpResponseRedirect(request.path_info)
        
        quiz = Quiz.objects.create(
            title = df['Quiz_Title'].iloc[0],
            topic = df['Topic'].iloc[0],
            description = df['Description'].iloc[0],
            time = df['Duration'].iloc[0],
            number_of_questions = df['Number of Questions'].iloc[0],
            image = image
        )
        
        counter = 0
        
        for question in df["Questions"]:
            new_question = Question.objects.create(
                text = question,
                quiz = quiz
            )
            
            for i in range(counter, counter+1):
                Answer.objects.create(text=df['Answer_1'].iloc[i], question=new_question)
                Answer.objects.create(text=df['Answer_2'].iloc[i], question=new_question)
                Answer.objects.create(text=df['Answer_correct'].iloc[i], question=new_question, correct=True)
                for j in df['Answer_4'].isna():
                    if j == False:
                        Answer.objects.create(text=df['Answer_4'].iloc[i], question=new_question)
            counter += 1
        messages.success(request, "Your quiz was successfully added!")    
        return redirect('quiz:index')     
    
    form = CsvImportForm()
    data = {'form': form}
    return render(request, 'upload_csv.html', data)


def results(request):
    results = Result.objects.all()
    return render(request, "results.html", {'results': results})    