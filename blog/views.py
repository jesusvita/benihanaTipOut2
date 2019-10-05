from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, tipOut
from .forms import personalTeppan
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import re

def add_items(y):
    x = 0
    add = re.findall('([-+]?\d*\.\d+|\d+)', y)
    for i in add:
        x += float(i)
    return x

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def tip(request):
    if request.method == "POST":
        form = personalTeppan(request.POST)
        if form.is_valid():
            teppan_item = form.save(commit=False)
            teppan_item.sushi = add_items(teppan_item.sushi)
            teppan_item.bar = add_items(teppan_item.bar)
            teppan_item.busser = round(float(teppan_item.teppan) * 0.01, 2)
            teppan_item.teppan = round(float(teppan_item.teppan) * 0.085, 2)
            teppan_item.sushi = round(teppan_item.sushi * 0.075, 2)
            teppan_item.bar = round(teppan_item.bar * 0.045, 2)
            teppan_item.total = round(teppan_item.busser + teppan_item.teppan + teppan_item.sushi + teppan_item.bar, 2)
            if teppan_item.tip != '':
                teppan_item.tip = round(float(teppan_item.tip) - teppan_item.total, 2)
            teppan_item.save()
            return redirect("/tipapp/" + str(teppan_item.id) + "/")
    else:
        form = personalTeppan()
    return render(request, 'blog/about.html', {'form': form}, {'title': 'tip'})

def benihana(request, id):
    if request.method == "POST":
        return redirect("/")
    else:
        tipOut.objects.get( id= str( int(id) - 1) ).delete()
        tipout = tipOut.objects.get(id=id)
        if tipout.tip == '':
            tip = tipout.tip
        else:
            tip = float(tipout.tip)
        return render(request, 'blog/tipOutTotal.html', {'tipout': tipout, 'tip':tip})
