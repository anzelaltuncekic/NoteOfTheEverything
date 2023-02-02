
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  authenticate , login
from django.http import HttpResponseRedirect,HttpResponse
from ChatBot.chat import chatbot_view
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .filters import *
from django.db.models import Q

is_debug = True
@login_required
def chatbot(request):
    if is_debug:
        print("Chatbot method is beginning...")

    user_sentence = request.GET['msg']
    if is_debug:
        print("\t User sentence: ", user_sentence)

    chat = chatbot_view(str(user_sentence))
    if is_debug:
        print("\t Chat: ", chat)

    return HttpResponse(chat)


def mainpage(request):
    user = request.user
    registereduser = RegisteredUser.objects.get(user=user)
    requested_user_type = user_type.objects.get(registereduser=registereduser)
    context = {'requested_user_type':requested_user_type}
    return render(request, 'home/mainpage.html', context)

def password_reset(request):
    return render(request, 'home/password_reset.html')

@login_required
def logout(request):
    return render(request, 'home/logout.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login( request,user)
            return redirect('note_list')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'home/loginpage.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            register = RegisteredUser(username=username, first_name=first_name, last_name=last_name, email=email, user=user)
            register.save()
            new_user_type = user_type(registereduser=register, user_type='U')
            new_user_type.save()
            return redirect('loginpage')

    context = {'form': form}
    return render(request, 'home/register.html' , context)

@login_required
def ShareNote(request):
    noteForm = Share_Note()
    imageForm=Note_Images()
    registereduser = request.user.registereduser
    mydict = {'form': noteForm,'imageForm':imageForm}
    if request.method == 'POST':
        noteForm = Share_Note(request.POST)
        images = request.FILES.getlist('images')
        if noteForm.is_valid():
            note_title = request.POST['note_title']
            note_description = request.POST['note_description']
            note_pagenumber= request.POST['note_pagenumber']
            note_subject = request.POST['note_subject']
            newNote = Note(note_title=note_title,note_description=note_description,note_pagenumber=note_pagenumber, note_subject=note_subject,registereduser=registereduser)
            newNote.save()

            for image in images:
                photo = NoteImages.objects.create(image=image, gallery=newNote)
            photo.save()


            return redirect('createnote-success')

    return render(request, 'home/ShareNote.html', context=mydict)

@login_required
def createnotesuccess(request):
    return render(request, 'home/createnote-success.html')

@login_required
def change_email(request):
    registereduser = request.user.registereduser
    form = ChangeEmailForm(instance=registereduser)
    if request.method =='POST':
        form = ChangeEmailForm(request.POST,instance=registereduser)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'home/change_email.html', context)

@login_required
def change_password(request):
    if request.method =='POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/')
        else:
            return redirect('home/change_password')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form}
    return render(request, 'home/change_password.html', context)

@login_required
def change_username(request):
    registereduser = request.user.registereduser
    ruser = User.objects.get(id=request.user.id)
    form = ChangeUsernameForm(instance=registereduser)

    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=registereduser)
        if form.is_valid():
            newusername = request.POST['username']
            ruser.username = newusername
            ruser.save()
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'home/change_username.html', context)


@login_required
def note_list(request):
    user = request.user
    registereduser = RegisteredUser.objects.get(user=user)
    requested_user_type = user_type.objects.get(registereduser=registereduser)
    pending_note = Note.objects.all().filter(note_status='P')
    filter_note = Note.objects.all().filter(note_status='A').order_by('-note_score') # - büyükten küçüğe(ascending)
    pending_comment_note = Comment.objects.all().filter(status="New")
    pending_comment_note_count = Comment.objects.all().filter(status="New").count()
    counter = 0


    if int(pending_comment_note_count) != 0:
        counter = int(pending_comment_note_count)

    query = request.GET.get('query')
    page_num_from = request.GET.get('page_num_from', 0)
    page_num_to = request.GET.get('page_num_to', 1000)
    score_from = request.GET.get('score_from', 0)
    score_to = request.GET.get('score_to', 5)

    if query != None:
        filter_note = filter_note.filter(Q(note_title__icontains = query) | Q(note_description__icontains = query) | Q(note_subject__icontains = query))
    else:
        query = ""

    filter_note = filter_note.filter(note_pagenumber__gte=page_num_from).filter(note_pagenumber__lte=page_num_to)
    filter_note = filter_note.filter(note_score__gte=score_from).filter(note_score__lte=score_to)
    myFilter = NoteFilter(request.GET , queryset=filter_note)
    filter_note = myFilter.qs
    notecount = filter_note.count()

    context = {
        'notecount':notecount,
        'filter_note': filter_note,
        'requested_user_type':requested_user_type,
        'pending_note':pending_note,
        'page_num_from':page_num_from,
        'page_num_to': page_num_to,
        'score_from':score_from,
        'score_to': score_to,
        'myFilter': myFilter,
        'query':query,
        'pending_comment_note':pending_comment_note,
        'counter':counter,

    }
    return render(request, 'home/note_list.html' , context )


@login_required
def note_details(request, id):
    user = request.user
    registereduser = RegisteredUser.objects.get(user=user)
    requested_user_type = user_type.objects.get(registereduser=registereduser)
    pending_note = Note.objects.all().filter(id=id, note_status='P')
    notes = Note.objects.get(id=id)
    note_image = NoteImages.objects.filter(gallery=notes)
    all_note = Note.objects.all().filter(id=id)
    favourite_notes = user.favourite.all().filter(id=id)
    form = CommentForm()
    comments = Comment.objects.all().filter(note_id=id, status="True")
    all_comments =Comment.objects.filter(note_id=id)

    commentid=0
    com=""

    for n in all_comments:
        commentid=n.id
        com=Comment.objects.filter(note_id=id).get(id=commentid)
        print("user:", com.registereduser)

    comments_count = Comment.objects.filter(note_id=id, status=True).count()
    my_comments_count = 0

    rating_count = []
    all_rating = 0

    for com in comments:
        rate = com.rating
        rating_count.append(rate)

    if(len(rating_count) != 0):
        all_rating = sum(rating_count) / len(rating_count)
        all_rating=round(all_rating,1)
        Note.objects.filter(id=id).update(note_score= all_rating)
    else:
        Note.objects.filter(id=id).update(note_score=0)

    doc_type = " "

    for i in note_image:
        doc_name = str(i.image).split('/')
        doc_title = str(doc_name[0])
        doc_split = str(doc_title).split('.')
        doc_type = str(doc_split[1])

    if int(comments_count) != 0:
        my_comments_count = int(comments_count)

    cuser=""

    form = CommentForm(request.POST)
    if request.method == 'POST':  # check post
        if form.is_valid():
            form = CommentForm(request.POST)
            comment = request.POST['comment']
            rating = request.POST['rating']
            comment_owner = request.POST['comment_owner']
            createat = datetime.datetime.now()
            newComment = Comment(note_id=id, comment=comment, rating=rating, create_at=createat,
                                 registereduser=registereduser, comment_owner=comment_owner)
            newComment.save()
            messages.success(request, "Your review has ben sent for approval. Thank you for your interest.")
            form = CommentForm()
    else:

        form = CommentForm()

    return render(request, 'home/note_details.html',
                  {'cuser': cuser, 'com': com, 'all_comments': all_comments, 'notes': notes,
                   'pending_note': pending_note, 'note_image': note_image, 'comments': comments, 'form': form,
                   'registereduser': registereduser, 'favourite_notes': favourite_notes, 'all_note': all_note,
                   'my_comments_count': my_comments_count, 'doc_type': doc_type, 'doc_title': doc_title,
                   'requested_user_type': requested_user_type, 'all_rating': all_rating, 'form': form})


@login_required
def my_notes(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    registered_user = RegisteredUser.objects.get(user=user)
    my_notes=Note.objects.filter(registereduser=registered_user).filter(note_status='A')
    my_notes_try = Note.objects.filter(registereduser=registered_user).filter(note_status='A').count()
    my_notes_count = 0

    if int(my_notes_try) != 0:
        my_notes_count = int(my_notes_try)

    return render(request, 'home/my_notes.html', {'my_notes': my_notes, 'my_notes_count':my_notes_count})

@login_required
def delete_note(request , id):
    Note.objects.get(id=id).delete()
    return redirect('/my_notes')

@login_required
def delete_fav_note(request , id):
    note = get_object_or_404(Note, id=id)
    if note.favourite.filter(id=request.user.id).exists():
        note.favourite.remove(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def note_favourite_list(request):
    user = request.user
    favourite_notes = user.favourite.all()
    favori_count = user.favourite.all().count()

    context = {
        'favourite_notes': favourite_notes,
        'favori_count':favori_count,
    }
    return render(request, 'home/note_favourite_list.html', context)

@login_required
def favourite_note(request, id):
    note = get_object_or_404(Note, id=id)
    note.favourite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def Cancelled_note(request , id):
    pending_note = Note.objects.all().filter(id=id).filter(note_status='P')
    pending_note.delete()
    return redirect('/note_list')

@login_required
def Approved_note(request , id):
    pending_note = Note.objects.all().filter(id=id).filter(note_status='P')
    pending_note.update(note_status='A')
    return redirect('/note_list')

@login_required
def admin_pending_notes(request):
    user = request.user
    registereduser = RegisteredUser.objects.get(user=user)
    requested_user_type = user_type.objects.get(registereduser=registereduser)
    pending_note = Note.objects.all().filter(note_status='P')
    pending_note_counts = Note.objects.filter(note_status='P').count()

    context = {
        'requested_user_type': requested_user_type,
        'pending_note': pending_note,
        'pending_note_counts':pending_note_counts,

    }
    return render(request, 'home/admin_pending_notes.html', context)

@login_required
def admin_pending_comments(request, id):
        user = request.user
        registereduser = RegisteredUser.objects.get(user=user)
        requested_user_type = user_type.objects.get(registereduser=registereduser)
        notes = Note.objects.get(id=id)
        note_image = NoteImages.objects.filter(gallery=notes)
        all_note = Note.objects.all().filter(id=id)

        pending_comments = Comment.objects.all().filter(note_id=id, status='New')
        print("pendings:", pending_comments)
        pending_comments_count = Comment.objects.filter(note_id=id).count()
        my_pending_comments_count = 0

        if int(pending_comments_count) != 0:
            my_pending_comments_count = int(pending_comments_count)

        doc_type = " "

        for i in note_image:
            doc_name = str(i.image).split('/')
            doc_title = str(doc_name[0])
            doc_split = str(doc_title).split('.')
            doc_type = str(doc_split[1])

        return render(request, 'home/admin_pending_comments.html',
                      {'notes': notes, 'pending_comments': pending_comments, 'note_image': note_image,
                       'registereduser': registereduser, 'all_note': all_note, 'doc_type': doc_type,
                       'doc_title': doc_title,
                       'requested_user_type': requested_user_type, 'pending_comments_count': pending_comments_count,
                       'my_pending_comments_count': my_pending_comments_count})

@login_required
def delete_comment(request , id):
    pending_comments = Comment.objects.all().filter(id=id, status='New')
    pending_comments.delete()
    return redirect('/note_list')

@login_required
def publish_comment(request , id):
    pending_comments = Comment.objects.all().filter(id=id, status='New')
    pending_comments.update(status='True')
    comment=Comment.objects.get(id=id)
    note_comment=int(comment.note.id)
    return redirect('note_details', id=note_comment)
