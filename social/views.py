from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from social import models, forms

# Create your views here.
class Wall(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name =  'social/wall.html'
    login_url = 'auth/login'

    def get_queryset(self):
        friendIds = [friend.person2.id for friend in models.Friends.objects.filter(person1 = self.request.user)]
        friendIds += [friend.person1.id for friend in models.Friends.objects.filter(person2 = self.request.user)]

        return models.Post.objects.filter(user__in = friendIds).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['comment_form'] = forms.PostComment
        return data

class Home(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name =  'social/home.html'
    login_url = 'auth/login'

    def get_queryset(self):
        return models.Post.objects.filter(user = self.request.user)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['post_form'] = forms.PostForm
        data['comment_form'] = forms.PostComment
        data['add_friend'] = forms.PostFriend
        return data

class Post(View):
    def post(self, request):
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        
        return redirect('/home/')

class Friends(View):
    def post(self, request):
        form = forms.PostFriend(request.POST, request.FILES)
        post = form.save(commit=False)
        flag = 0
        for person in models.Friends.objects.filter(person1 = request.user):
            print(person.person2,post.person2)
            if post.person2 == person.person2 or post.person2 == request.user:
                print('exists')
                flag = 1

        if form.is_valid() and flag == 0:
            post.person1 = request.user
            post.save()  
            print('added')      
        return redirect('/profile/')
                
        

def profile(request):
    context = {
        "friends": models.Friends.objects.filter(person1 = request.user),
    }
    return render(request, 'social/profile.html', context)

class PostLike(View):
    model = models.Post

    def post(self, request, pk):
        post = self.model.objects.get(pk = pk)
        models.Like.objects.create(post = post, user = request.user)
        return HttpResponse(code = 204)

class PostComment(View):
    model = models.Post
    def post(self, request, pk):
        form = forms.PostComment(request.POST, request.FILES)

        


        if form.is_valid():           
            comment = form.save(commit=False)
            comment.user = request.user
            print(pk,request.user,self.post)
            post = self.model.objects.get(pk = pk)
            comment.post = post
            comment.save()
        
        return redirect('/home/')

class PostLike(View):
    model = models.Post

    def post(self, request, pk):
        form = forms.PostLike(request.POST, request.FILES)
        post = self.model.objects.get(pk = pk)
        flag = 0
        for like in models.Like.objects.all():
            if like.user == request.user and like.post == post:
                flag = 1
                print('liked')

        if form.is_valid() and flag == 0:
            like = form.save(commit=False)
            like.user = request.user
            like.post = post
            like.save()
        return redirect('/')



# class PostComment(View):
#     model = models.Post
#     form = forms.PostComment

#     def post(self, request, pk):
#         post = self.model.objects.get(pk = pk)
#         form = self.form(request.POST, request.FILES)

#         if form.is_valid():
#             comment = form.save(commit = False)
#             comment.post = post
#             comment.user = request.user
#             comment.save()
#             # return HttpResponse(code = 204)
#             return redirect('/home/')
    
#         print(form.errors)
#         # return HttpResponse('Error')
#         return render(request, 'home.html', {'comment_form': form})
