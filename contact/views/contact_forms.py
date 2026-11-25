# render -> Renderiza um template HTML e devolve uma resposta HTTP
# redirect -> Redireciona o usuário para outra URL
# get_object_or_404 -> Busca um registro no banco; se não existir, retorna erro 404
# reverse -> Obtém uma URL a partir do nome definido no urls.py
# ContactForm -> Formulário utilizado para cadastrar/editar contatos
# Contact -> Model que representa os contatos no banco


from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact

def create(request):
    # procura a rota contact:create no sistema de URLs do Django e gera sua URL
    # depois será enviada ao HTML através de form_action.
    form_action = reverse('contact:create')

    # Django cria um ContactForm contendo os dados enviados.
    if request.method == 'POST':
        form = ContactForm(request.POST)


        # Context transporta informações da view Python para o template HTML
        context = {
            'form': form,
            'form_action': form_action,
        }

	# Verifica se os dados enviados atendem às regras definidas no ContactForm e no model.
        if form.is_valid():
	    # Contato é salvo no banco de dados e 
	    # contact - representa o contato que acabou de ser cadastrado
            contact = form.save()
	    # Usuário é então redirecionado para a página de edição desse contato
            return redirect('contact:update', contact_id=contact.pk)

	# página é apresentada novamente
        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )



def update(request, contact_id):
    # procura no banco um contato que satisfaça as duas condições
    # se encontrar, o objeto é armazenado em contact
    # se não encontrar, retorna automaticamente uma página HTTP 404 — Not Found
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )
    # reverse() gera a URL da atualização daquele contato específico -> /contact/25/update/
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
	# informa para utilizar os dados enviados para alterar este contato que já existe.
	# sem instance=contact, o formulário poderia ser tratado como a criação de um novo objeto, em vez da edição do existente.
        form = ContactForm(request.POST, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )

def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
