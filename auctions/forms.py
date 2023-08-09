from django import forms
from .models import Comment
from .models import AuctionListing


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ('current_bid', 'seller')  # Exclude current_bid and seller fields
        

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super(AuctionListingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AuctionListingForm, self).save(commit=False)
        instance.seller = self.user  # Set the seller to the logged-in user
        if commit:
            instance.save()
        return instance
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']




