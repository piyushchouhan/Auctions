from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from auctions.forms import CommentForm, EditCommentForm
from auctions.models import User, AuctionListing, Comment
from django.contrib import messages

# Create your views here.

def all_listing(request):
    listing = AuctionListing.objects.all()
    return render(request, 'listing/all_listing.html', {'listings': listing})



def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    comments = Comment.objects.filter(listing=listing)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Login required to comment.')
            return redirect('listing_detail', listing_id=listing_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid(): 
            new_comment = comment_form.save(commit=False)
            new_comment.listing = listing
            new_comment.commenter = request.user
            new_comment.save()
            return redirect('listing_detail', listing_id=listing_id)
    else:
        comment_form = CommentForm()

    return render(request, 'listing/listing.html', {
        'listing': listing,
        'comments': comments,
        'comment_form': comment_form,
    })


def delete_comment(request, comment_id, listing_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.commenter:
        comment.delete()
    return redirect('listing_detail', listing_id=listing_id)

@login_required(login_url='auctions/login.html')
def user(request, user_id):
    user = User.objects.get(pk = user_id)
    return render(request, 'listing/user.html', {'user': user})

def editComment(request, listing_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.commenter:
        return redirect('listing_detail', listing_id=listing_id)
    
    if request.method == "POST":
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', listing_id=listing_id)
    else:
        form = EditCommentForm(instance=comment)
        
    return render(request, 'listing/edit_comment.html', {'form': form, 'listing_id': listing_id})

def delete_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user == listing.seller:
        listing.delete()
    return redirect('all_listing')
    

