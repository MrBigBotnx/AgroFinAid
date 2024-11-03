
from django.shortcuts import render, get_object_or_404, redirect
from .models import Beneficiario, Financiamento, Atividade, Amortizacao
from .forms import BeneficiarioForm, FinanciamentoForm, AtividadeForm, AmortizacaoForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



# View para criar um novo beneficiário
def criar_beneficiario(request):
    if request.method == 'POST':
        form = BeneficiarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_beneficiarios')  # Redireciona para uma lista de beneficiários, que vamos criar depois
    else:
        form = BeneficiarioForm()
    return render(request, 'base/criar_beneficiario.html', {'form': form})

# View para editar um beneficiário existente
def editar_beneficiario(request, id):
    beneficiario = get_object_or_404(Beneficiario, id=id)
    if request.method == 'POST':
        form = BeneficiarioForm(request.POST, instance=beneficiario)
        if form.is_valid():
            form.save()
            return redirect('listar_beneficiarios')
    else:
        form = BeneficiarioForm(instance=beneficiario)
    return render(request, 'base/editar_beneficiario.html', {'form': form})

# Repetimos o mesmo processo para Financiamento, Atividade e Amortizacao
# View para criar um financiamento
def criar_financiamento(request):
    if request.method == 'POST':
        form = FinanciamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_financiamentos')
    else:
        form = FinanciamentoForm()
    return render(request, 'base/criar_financiamento.html', {'form': form})

# View para editar um financiamento existente
def editar_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    if request.method == 'POST':
        form = FinanciamentoForm(request.POST, instance=financiamento)
        if form.is_valid():
            form.save()
            return redirect('listar_financiamentos')
    else:
        form = FinanciamentoForm(instance=financiamento)
    return render(request, 'base/editar_financiamento.html', {'form': form})

# View para criar uma atividade
def criar_atividade(request):
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm()
    return render(request, 'base/criar_atividade.html', {'form': form})

# View para editar uma atividade existente
def editar_atividade(request, id):
    atividade = get_object_or_404(Atividade, id=id)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm(instance=atividade)
    return render(request, 'base/editar_atividade.html', {'form': form})

# View para criar uma amortização
def criar_amortizacao(request):
    if request.method == 'POST':
        form = AmortizacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_amortizacoes')
    else:
        form = AmortizacaoForm()
    return render(request, 'base/criar_amortizacao.html', {'form': form})

# View para editar uma amortização existente
def editar_amortizacao(request, id):
    amortizacao = get_object_or_404(Amortizacao, id=id)
    if request.method == 'POST':
        form = AmortizacaoForm(request.POST, instance=amortizacao)
        if form.is_valid():
            form.save()
            return redirect('listar_amortizacoes')
    else:
        form = AmortizacaoForm(instance=amortizacao)
    return render(request, 'base/editar_amortizacao.html', {'form': form})


# base/views.py
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$',
                message="Digite um endereço de e-mail válido."
            )
        ]
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message="A senha deve ter no mínimo 8 caracteres, incluindo letras e números."
            )
        ]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

def register(request):
    if request.method == 'POST':
        # Capturar os dados do formulário manualmente
        username = request.POST['username']
        email = request.POST['email']
        idade = request.POST['idade']
        tipo_atividade = request.POST['tipo_atividade']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validação básica
        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'base/register.html')

        # Criar o usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Criar o beneficiário associado
        Beneficiario.objects.create(
            usuario=user,
            nome_completo=username,
            idade=idade,
            tipo_atividade=tipo_atividade,
            historico_financiamentos=""
        )

        # Logar o usuário automaticamente após o registro
        login(request, user)
        messages.success(request, "Registro realizado com sucesso!")
        return redirect('login')  # Redireciona para o login após o registro

    return render(request, 'base/register.html')

@csrf_exempt
def ajax_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Usuário já existe.'})

        # Cria o usuário e salva no banco de dados
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'success': True, 'message': 'Registro criado com sucesso!'})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # Defina a URL desejada
    return render(request, 'login.html')

@csrf_exempt
def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Usuário ou senha incorretos.'})

@login_required
def dashboard(request):
    try:
        beneficiario = Beneficiario.objects.get(usuario=request.user)
        financiamentos = Financiamento.objects.filter(beneficiario=beneficiario)
    except Beneficiario.DoesNotExist:
        financiamentos = []

    return render(request, 'base/dashboard.html', {'financiamentos': financiamentos})


def listar_financiamentos(request):
    # Buscar o beneficiário logado (assumindo que o usuário é um beneficiário)
    beneficiario = Beneficiario.objects.get(usuario=request.user)
    
    # Buscar financiamentos desse beneficiário
    fund_requests = Financiamento.objects.filter(beneficiario=beneficiario)
    
    # Passar os dados para o template
    return render(request, 'base/fund_requests.html', {'fund_requests': fund_requests})

from django.forms.models import model_to_dict
@login_required
@csrf_exempt
def solicitar_financiamento(request):
    if request.method == 'POST':
        financiamento_form = FinanciamentoForm(request.POST)
        atividade_form = AtividadeForm(request.POST)

        if financiamento_form.is_valid() and atividade_form.is_valid():
            try:
                beneficiario = Beneficiario.objects.get(usuario=request.user)
            except Beneficiario.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Beneficiário não encontrado.'})

            # Salva o financiamento e associa ao beneficiário
            financiamento = financiamento_form.save(commit=False)
            financiamento.beneficiario = beneficiario
            financiamento.save()

            # Reatribui o financiamento ao formulário de atividade
            atividade = atividade_form.save(commit=False)
            atividade.financiamento = financiamento  # Define o financiamento criado
            atividade.save()

            return JsonResponse({'success': True, 'message': 'Solicitação de financiamento criada com sucesso!'})

        # Captura erros específicos dos formulários
        errors = {
            'financiamento_form_errors': financiamento_form.errors,
            'atividade_form_errors': atividade_form.errors
        }
        return JsonResponse({'success': False, 'message': 'Erro ao validar os dados do formulário.', 'errors': errors})

    # GET request
    financiamento_form = FinanciamentoForm()
    atividade_form = AtividadeForm()
    return render(request, 'base/solicitar_financiamento.html', {
        'financiamento_form': financiamento_form,
        'atividade_form': atividade_form
    })

def view_fund_request(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    atividades = Atividade.objects.filter(financiamento=financiamento)  # Busca todas as atividades relacionadas
    return render(request, 'base/view_fund_request.html', {
        'financiamento': financiamento,
        'atividades': atividades
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Financiamento, Atividade
from .forms import FinanciamentoForm, AtividadeForm

def editar_financiamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    
    if request.method == 'POST':
        financiamento_form = FinanciamentoForm(request.POST, instance=financiamento)
        atividade_form = AtividadeForm(request.POST)
        
        if financiamento_form.is_valid() and atividade_form.is_valid():
            # Salva o formulário de Financiamento
            financiamento_form.save()
            
            # Define o financiamento_id para a atividade e salva
            atividade = atividade_form.save(commit=False)
            atividade.financiamento = financiamento
            atividade.save()
            
            return redirect('dashboard')
    else:
        financiamento_form = FinanciamentoForm(instance=financiamento)
        atividade_form = AtividadeForm()

    return render(request, 'base/editar_financiamento.html', {
        'financiamento_form': financiamento_form,
        'atividade_form': atividade_form
    })


def landing_page(request):
    return render(request, 'base/landing_page.html')


import pdfkit
from django.shortcuts import render
from django.http import HttpResponse
from .models import Financiamento
from django.template.loader import render_to_string

def gerar_relatorio_pdf(request):
    beneficiario_id = request.user.id
    financiamentos = Financiamento.objects.filter(beneficiario__id=beneficiario_id)

    html_content = render_to_string('base/relatorio_pdf_template.html', {'financiamentos': financiamentos})
    
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }

    # Especifique o caminho do executável wkhtmltopdf
    path_to_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Altere este caminho conforme necessário
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_financiamentos.pdf"'
    return response

@login_required
def detalhes_financiamento(request, financiamento_id):
    financiamento = get_object_or_404(Financiamento, id=financiamento_id)
    amortizacoes = financiamento.amortizacao_set.all()
    return render(request, 'base/detalhes_financiamento.html', {
        'financiamento': financiamento,
        'amortizacoes': amortizacoes
    })


@login_required
def amortizacao_geral(request):
    financiamentos = Financiamento.objects.all()
    return render(request, 'base/amortizacao_geral.html', {'financiamentos': financiamentos})

@login_required
def selecionar_financiamento(request):
    beneficiario = request.user.beneficiario
    financiamentos = Financiamento.objects.filter(beneficiario=beneficiario)
    return render(request, 'base/selecionar_financiamento.html', {'financiamentos': financiamentos})

