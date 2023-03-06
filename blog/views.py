
from .forms import PostForm, CommentForm
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.views.decorators.csrf import csrf_protect
from django.views import View
from django.utils.decorators import method_decorator


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    # Redirect to a success page.
    
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)




class AddBookView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        with open("blog/data.json") as f:
            data = json.load(f)
        return render(request, 'blog/add_book.html')
        
    @method_decorator(csrf_protect)
    def post(self, request):
        with open("blog/data.json") as f:
            data = json.load(f)
        bookNameList = data['BookNameList']
        bookAuthorList = data['BookAuthorList']
        bookGenreList = data['BookGenreList']
        bookAvailable = data['BookAvailable']

        # handle form submission
        book_name = request.POST.get('book_name')
        book_author = request.POST.get('book_author')
        book_genre = request.POST.get('book_genre')
        book_available = request.POST.get('book_available', False)
        if book_available:
            book_available = 1
        else:
            book_available = 0

        # add book to list and save to database
        bookNameList.append(book_name)
        bookAuthorList.append(book_author)
        bookGenreList.append(book_genre)
        bookAvailable.append(book_available)
        data = {"BookNameList": bookNameList, "BookGenreList": bookGenreList, "BookAuthorList": bookAuthorList, "BookAvailable": bookAvailable}
        with open("blog/data.json", "w") as f:
            json.dump(data, f)
        return render(request, 'blog/add_book.html')
    
    
class bookListView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        search = request.GET.get('q')
        with open("blog/data.json") as f:
            data = json.load(f)
            
        bookNameList = data['BookNameList']
        bookAuthorList = data['BookAuthorList']
        bookGenreList = data['BookGenreList']
        bookAvailable = data['BookAvailable']
        
        if search in bookNameList:
            position = bookNameList.index(search)
            foundName = bookNameList[position]
            foundAuthor = bookAuthorList[position]
            foundGenre = bookGenreList[position]
            foundAvail = bookAvailable[position]
            
            placeholder1 = position  # initialize placeholder1 with position
            placeholder = {'Position': placeholder1}
            with open("blog/position.json", "w") as f:
                json.dump(placeholder, f)
            
            if foundAvail == 1:
                foundAvail = 'Yes'
            else:
                foundAvail='No'
            
            message = ''
        else:
            foundName = ""
            foundAuthor = ""
            foundGenre = ""
            foundAvail = ""
            message = f"No books found containing '{search}'"
            
        books = zip(bookNameList, bookAuthorList, bookGenreList, bookAvailable)
        


        
        
        return render(request, 'blog/book_list.html', {'books': books, 'message': message, 
                                                       'foundName': foundName, 
                                                       'foundAuthor': foundAuthor, 
                                                       'foundGenre': foundGenre, 
                                                       'foundAvail': foundAvail,
                                                       'search': search  # Add the search parameter to the context
                                                       })

    def post(self, request):
        with open("blog/data.json") as f:
            data = json.load(f)
        bookNameList = data['BookNameList']
        bookAuthorList = data['BookAuthorList']
        bookGenreList = data['BookGenreList']
        bookAvailable = data['BookAvailable']
        
        with open("blog/position.json") as p:
            getposition = json.load(p)   #I know this would never work on a website with multiple people
            
        position = getposition['Position']
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            
            
            
            if action == 'check_in':
                bookAvailable[position] = 1
                data = {"BookNameList": bookNameList, "BookGenreList": bookGenreList, "BookAuthorList": bookAuthorList, "BookAvailable": bookAvailable}
                with open("blog/data.json", "w") as f:
                     json.dump(data, f)
                return redirect('book_list')
            
            
            elif action == 'check_out':
                bookAvailable[position] = 0
                
                data = {"BookNameList": bookNameList, "BookGenreList": bookGenreList, "BookAuthorList": bookAuthorList, "BookAvailable": bookAvailable}
                with open("blog/data.json", "w") as f:
                   json.dump(data, f)
                return redirect('book_list')
            
            
            
            elif action == 'delete':
                deleteName = bookNameList[position]
                deleteAuthor = bookAuthorList[position]
                deleteGenre = bookGenreList[position]
                deleteAvail = bookAvailable[position]
                
                bookNameList.remove(deleteName)
                bookAuthorList.remove(deleteAuthor)
                bookGenreList.remove(deleteGenre)
                bookAvailable.remove(deleteAvail)
                
                data = {"BookNameList": bookNameList, "BookGenreList": bookGenreList, "BookAuthorList": bookAuthorList, "BookAvailable": bookAvailable}
                with open("blog/data.json", "w") as f:
                     json.dump(data, f)
                     return redirect('book_list')
