
from django import forms
from .models import Comment,Transaction
from user_accounts.models import UserAccount
class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['name', 'email', 'body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # Make the 'email' field optional
        self.fields['email'].required = False
        


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type',
            'book'
           
            
        ]

# transaction er kj hobe backend theke. user transaction choice jate nh korte pare
        # user er account pass korsi aikhane
    def __init__(self, *args, **kwargs):
        # self.account a  user account save korsi
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    #save korar jonno
    def save(self, commit=True):
        # j user rwquest kortese tar object jodi database a thake shei instance er account a jabo
        self.instance.account = self.account
        # new balance dia update korsi.  500 tk ase. deposit korbo 300. total=800
        self.instance.balance_after_transaction = self.account.balance  # 0--->5000
        self.instance.paid = False
        return super().save()



 # Transaction form theke inherite korbe deposit
class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount