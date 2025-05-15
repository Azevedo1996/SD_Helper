import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

EXCEL_FILE_PATH = settings.BASE_DIR / 'todos_documentos' / 'troubleshooting.xlsx'

def carregar_planilha(path):
    """Carrega todas as abas de uma planilha Excel em um dicionário de DataFrames."""
    try:
        return pd.read_excel(path, sheet_name=None)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {path}")
        return {}

class IndexView(View):
    def get(self, request):
        fluxos_data = carregar_planilha(EXCEL_FILE_PATH)
        aplicacoes = list(fluxos_data.keys())
        return render(request, 'index.html', {'aplicacoes': aplicacoes})

class FlowView(View):
    def get(self, request, aplicacao, node_id=None):
        fluxos_data = carregar_planilha(EXCEL_FILE_PATH)
        if aplicacao not in fluxos_data:
            return render(request, 'error.html', {'mensagem': f'Aplicação "{aplicacao}" não encontrada.'})

        fluxo = fluxos_data[aplicacao].set_index('ID')

        if node_id is None:
            # Inicia o fluxo pelo primeiro nó (assumindo que o primeiro ID na planilha é o início)
            if not fluxo.empty:
                primeiro_node_id = fluxo.index[0]
                return redirect('flow', aplicacao=aplicacao, node_id=primeiro_node_id)
            else:
                return render(request, 'error.html', {'mensagem': f'Fluxo vazio para a aplicação "{aplicacao}".'})

        if node_id not in fluxo.index:
            return render(request, 'error.html', {'mensagem': f'Nó "{node_id}" não encontrado no fluxo de "{aplicacao}".'})

        no_atual = fluxo.loc[node_id]

        context = {
            'aplicacao': aplicacao,
            'tipo': no_atual['Tipo'],
            'texto': no_atual['Texto'],
            'node_id': node_id,
        }

        if no_atual['Tipo'] == 'pergunta':
            context['proximo_sim'] = no_atual['Próx. Sim']
            context['proximo_nao'] = no_atual['Próx. Não']
        elif no_atual['Tipo'] == 'solucao':
            pass  # Não há próximas opções para uma solução

        return render(request, 'flow.html', context)