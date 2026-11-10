from django.shortcuts import render
from contact.models import Contact

# Create your views here.

def index(request, contact_id):
    contacts = Contact.objects.all().order_by('-id')

    contacts = Contact.objects\
    .filter(show=True)\
    .order_by('-id')[:10]

    print(contacts.query) #mostra a consulta SQL
    
    context = {
            'contacts': contacts,
        }

    return render(
        request,
        'contact/index.html',
        context
    )