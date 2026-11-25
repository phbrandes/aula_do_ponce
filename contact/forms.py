# Importa o módulo de formulários do Django
# Importa a classe utilizada para criar erros de validação
# Importa os models da aplicação atua
from django import forms
from django.core.exceptions import ValidationError
from . import models

# Cria um formulário baseado no Model Contact
class ContactForm(forms.ModelForm):

    # Redefine manualmente o campo first_name.
    # Mesmo que esse campo exista no Model Contact,
    # podemos declará-lo aqui para personalizar sua apresentação e seu comportamento no formulário.
    first_name = forms.CharField(
	# Define o widget HTML utilizado pelo campo
        widget=forms.TextInput(
            attrs={
        	# Adiciona classes SS ao campo
                'class': 'classe-a classe-b',
        	# Define o texto exibido dentro do campo enquanto o usuário ainda não digitou nada
                'placeholder': 'Aqui veio do init',
            }
        ),
	# Texto utilizado como rótulo do campo
        label='Primeiro Nome',
	# Texto auxiliar que pode ser apresentado próximo ao campo no formulário
        help_text='Texto de ajuda para seu usuário',
    )
    # Método construtor do formulário.
    # É executado sempre que um ContactForm é criado.
    # *args recebe argumentos posicionais. **kwargs recebe argumentos nomeados.
    # Permite que o formulário receba, por exemplo: request.POST, instance=contact
    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe ModelForm.
        # É necessário para que o Django inicialize corretamente os campos e demais recursos do formulário.
        super().__init__(*args, **kwargs)
    # Classe interna utilizada para configurar o ModelForm.   
    class Meta:
        # Define que este formulário está associado ao Model Contact. 
        model = models.Contact
        fields = (
            'first_name','last_name','phone',
            'email','description','category',
        )

    # Método utilizado para realizar validações personalizadas nos dados do formulário
    # É executado durante o processo de validação iniciado por form.is_valid()  
    def clean(self):
	# Obtém os dados que passaram pelo processo de limpeza/validação dos campos
        cleaned_data = self.cleaned_data
	# Recupera o valor informado no campo first_name, get() é utilizado para evitar erro caso o campo não esteja disponível em cleaned_data.
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
	
	# Verifica uma regra personalizada, primeiro nome e sobrenome não podem ser iguais
        if first_name == last_name:
            # Cria uma mensagem de erro de validação
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
	     # Associa a mensagem de erro aos campos
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)