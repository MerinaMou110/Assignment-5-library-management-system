from django.shortcuts import render
from . import models 
from . import forms
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from user_accounts.models import UserAccount
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib import messages
from Library.constants import DEPOSIT,BOOK_RETURN
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Sum
from django.views.generic import CreateView, ListView

from Library.forms import (
    DepositForm
)
from Library.models import Transaction,Book

# Create your views here.

def send_transection_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


def send_borrowing_email(user, book, transaction, subject, template):
    message = render_to_string(template, {
        'user': user,
        'book': book,
        'transaction': transaction,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'library_details.html'

    def post(self, request, *args, **kwargs):
        print("Post method is being executed.")
        comment_form = forms.CommentForm(data=self.request.POST)
        book = self.get_object()
        print(f"Book ID: {book.id}, Borrowed: {book.borrow_book}")
        # Check if the user has borrowed the book
        if book.borrow_book:
            
        
            if comment_form.is_valid():
                print("Comment form is valid.")
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.save()
                print("Comment saved successfully.")
            else:
                print("Comment form is NOT valid.")
                print(comment_form.errors)
            return self.get(request, *args, **kwargs)
        else:
            print("Transaction does not exist.")
            messages.error(request, 'You can only review books that you have borrowed.')
            return redirect('detail_book', id=book.id)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book= self.object # post model er object ekhane store korlam
         # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # User is authenticated, access email attribute
            user_email = self.request.user.email
        else:
            # User is not authenticated, handle accordingly (e.g., set to None)
            user_email = None

        comments = book.comments.all()
        comment_form = forms.CommentForm(initial={'email': user_email})
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    #loading time komanor jonno reverse lazy use kora hoy
    success_url = reverse_lazy('update_profile')

     
    # jokhn obj toiri hobe tokhn e jodi kono kaj korte chai tahole get_form_kwargs
    # views theke kaj kortesi
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context



class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        send_transection_email(self.request.user, amount, "Deposite Message", "deposite_email.html")

        return super().form_valid(form)




@login_required
def borrow_book(request, book_id):
    
    book = get_object_or_404(Book, id=book_id)
    user_account = request.user.account
    

    if user_account.balance >= book.borrowing_price:
        # Sufficient balance to borrow the book
        user_account.balance -= book.borrowing_price
        
        
        book.borrow_book=True
        book.save()
        

        user_account.save()

        # Set the borrowing date
        borrowing_date = datetime.now()

        # Create a transaction record
        Transaction.objects.create(
            account=user_account,
            book=book,
            amount=book.borrowing_price,
            balance_after_transaction=user_account.balance,
            transaction_type=BOOK_RETURN,  
            timestamp=borrowing_date,
            paid=False,
            borrowing_date=borrowing_date
        )

        # Perform any additional book borrowing logic here

        messages.success(request, f'You have successfully borrowed "{book.title}".')
        transactions = Transaction.objects.all()
        send_borrowing_email(request.user, book, transactions, "Borrowed Book Message", "borrowed_book_email.html")
    else:
        # Insufficient balance
        messages.error(request, 'You do not have enough balance to borrow this book.')

       


    return redirect('detail_book', id=book_id)



class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        # jodi user kono type filter nh kore taile tar total transition report dekhabo
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            

            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
        queryset = queryset.select_related('book') 
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'borrowing_history': context['object_list'],  # Rename 'transactions' to 'borrowing_history'

        })

        return context
    



@login_required
def return_book(request, transaction_id):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        transaction = get_object_or_404(Transaction, id=transaction_id)

        # Check if the book hasn't been paid yet
        if not transaction.paid :
            # Update the balance
            user_account = request.user.account
            user_account.balance += transaction.amount
            user_account.save()
            
            # Update the transaction record
            transaction.paid = True
            transaction.save()
            

            messages.success(request, 'Book returned successfully.')
        else:
            messages.error(request, 'Invalid transaction.')

    return redirect('profile')
