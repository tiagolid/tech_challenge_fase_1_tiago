"""Tabelas para o relatório no Power BI, com as mesmas regras dos notebooks.

A tabela de pedidos (fato_pedidos) recebe os KPIs como medidas DAX. Os achados que dependem
de contas mais longas (recompra por nota, etapas da entrega, distância, previsão, temas dos
comentários) saem prontos daqui, para o Power BI mostrar exatamente o número dos notebooks.
O arquivo conferencia_kpis.csv traz o valor esperado de cada medida.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTO = RAIZ / 'data' / 'raw'
SAIDA = RAIZ / 'data' / 'powerbi'
SAIDA.mkdir(parents=True, exist_ok=True)
INICIO, FIM = '2017-01-01', '2018-08-31 23:59:59'


def grava(tabela, nome):
    tabela.to_csv(SAIDA / f'{nome}.csv', index=False, encoding='utf-8')
    print(f'{nome}: {len(tabela):,} linhas')


def nome_categoria(texto):
    return texto.replace('_', ' ')


orders = pd.read_csv(BRUTO / 'olist_orders_dataset.csv')
for coluna in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
               'order_delivered_customer_date', 'order_estimated_delivery_date']:
    orders[coluna] = pd.to_datetime(orders[coluna])
items = pd.read_csv(BRUTO / 'olist_order_items_dataset.csv')
items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
payments = pd.read_csv(BRUTO / 'olist_order_payments_dataset.csv')
reviews = pd.read_csv(BRUTO / 'olist_order_reviews_dataset.csv')
for coluna in ['review_creation_date', 'review_answer_timestamp']:
    reviews[coluna] = pd.to_datetime(reviews[coluna])
customers = pd.read_csv(BRUTO / 'olist_customers_dataset.csv')
sellers = pd.read_csv(BRUTO / 'olist_sellers_dataset.csv')
products = pd.read_csv(BRUTO / 'olist_products_dataset.csv')
geolocation = pd.read_csv(BRUTO / 'olist_geolocation_dataset.csv')
pedidos = pd.read_csv(RAIZ / 'data' / 'processed' / 'pedidos.csv')
populacao = pd.read_csv(RAIZ / 'data' / 'external' / 'populacao_uf_2018_ibge.csv')

nota_pedido = reviews.sort_values('review_answer_timestamp').drop_duplicates(subset='order_id', keep='last')

# fato_pedidos: um pedido por linha, só o recorte
fato = pedidos[pedidos['no_recorte']].copy()
compra = pd.to_datetime(fato['order_purchase_timestamp'])
fato = pd.DataFrame({
    'pedido': fato['order_id'],
    'cliente': fato['customer_unique_id'],
    'status': fato['order_status'],
    'data_compra': compra.dt.date,
    'mes': compra.dt.to_period('M').dt.to_timestamp().dt.date,
    'venda_valida': fato['venda_valida'],
    'entregue': fato['entregue'],
    'atrasado': fato['atrasado'].map({1.0: True, 0.0: False}),
    'uf_cliente': fato['uf_cliente'],
    'uf_vendedor': fato['uf_seller'],
    'categoria': fato['categoria'].fillna('sem categoria').map(nome_categoria),
    'meio_pagamento': fato['meio_pagamento'],
    'parcelas': fato['parcelas'],
    'valor_produtos': fato['valor_produtos'].round(2),
    'valor_frete': fato['valor_frete'].round(2),
    'valor_vendido': fato['receita'].round(2),
    'nota': fato['nota'],
    'dias_entrega': fato['dias_entrega'].round(2),
    'dias_vs_prometido': fato['dias_vs_prometido'],
})
grava(fato, 'fato_pedidos')
grava(populacao, 'dim_estado')

# achado 3: formas de pagamento (notebook 02, item 3.6)
nomes_pagamento = {'credit_card': 'Cartão de crédito', 'boleto': 'Boleto', 'voucher': 'Voucher',
                   'debit_card': 'Cartão de débito'}
pagamentos = payments['payment_type'].value_counts(normalize=True).rename('pct_pagamentos').to_frame()
pagamentos['parcelas_mediana'] = payments.groupby('payment_type')['payment_installments'].median()
pagamentos = pagamentos.drop('not_defined').rename(index=nomes_pagamento).rename_axis('forma_pagamento').reset_index()
grava(pagamentos.round(4), 't_pagamentos')

# achado 7: categorias pelo valor dos itens (notebook 04, item 7.2)
vendas_itens = orders[orders['order_purchase_timestamp'].between(INICIO, FIM)
                      & ~orders['order_status'].isin(['canceled', 'unavailable'])]
itens_vendidos = items[items['order_id'].isin(vendas_itens['order_id'])].copy()
itens_vendidos['valor'] = itens_vendidos['price'] + itens_vendidos['freight_value']
itens_vendidos = itens_vendidos.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
itens_vendidos['categoria'] = itens_vendidos['product_category_name'].fillna('sem categoria').map(nome_categoria)
categorias = itens_vendidos.groupby('categoria')['valor'].sum().sort_values(ascending=False).rename('valor_vendido').to_frame()
categorias['pct_valor_vendido'] = categorias['valor_vendido'] / categorias['valor_vendido'].sum()
categorias['posicao'] = range(1, len(categorias) + 1)
grava(categorias.reset_index().round(4), 't_categorias')

# base de entregues dos notebooks 03 e 04
entregues = orders[(orders['order_status'] == 'delivered')
                   & orders['order_delivered_customer_date'].notna()
                   & orders['order_purchase_timestamp'].between(INICIO, FIM)].copy()
entregues['dia_entrega'] = entregues['order_delivered_customer_date'].dt.normalize()
entregues['atrasado'] = entregues['dia_entrega'] > entregues['order_estimated_delivery_date']
entregues = entregues.merge(nota_pedido[['order_id', 'review_score', 'review_creation_date']], on='order_id', how='left')
entregues['nota_ruim'] = entregues['review_score'] <= 2

# achado 4: quando o cliente atrasado avalia (notebook 03, item 4.7)
atrasados = entregues[entregues['atrasado']].copy()
atrasados['momento'] = np.where(atrasados['review_creation_date'] < atrasados['dia_entrega'],
                                'Antes de receber', 'Depois de receber')
momento = atrasados.groupby('momento').agg(pedidos=('order_id', 'size'), pct_notas_1_2=('nota_ruim', 'mean'))
momento['pct_dos_atrasados'] = momento['pedidos'] / momento['pedidos'].sum()
grava(momento.reset_index().round(4), 't_avaliacao_atrasados')

# achado 10: quem escreve comentário, por nota (notebook 03, item 4.9)
comentarios = nota_pedido.groupby('review_score').agg(avaliacoes=('review_id', 'size'),
                                                      pct_com_comentario=('review_comment_message', lambda s: s.notna().mean()))
grava(comentarios.rename_axis('nota').reset_index().round(4), 't_comentarios_por_nota')

# achado 9: temas dos comentários (IA, docs/temas_comentarios)
linhas = []
for nota in range(1, 6):
    texto = (RAIZ / 'docs' / 'temas_comentarios' / f'nota_{nota}.md').read_text(encoding='utf-8')
    for linha in texto.splitlines():
        partes = [p.strip() for p in linha.strip().strip('|').split('|')]
        if len(partes) == 4 and partes[0].isdigit():
            numeros = [int(n) for n in re.findall(r'(\d+)%', partes[3])]
            linhas.append({'nota': nota, 'posicao': int(partes[0]), 'tema': partes[1].replace('**', ''),
                           'parcela_estimada': partes[3].replace('**', ''),
                           'parcela_aprox': sum(numeros) / len(numeros) / 100 if numeros else None})
grava(pd.DataFrame(linhas), 't_temas_comentarios')

# achado 5: recompra pela nota do primeiro pedido (notebook 03, itens 5.2 e 5.3)
vendas_clientes = orders.merge(customers, on='customer_id')
vendas_clientes = vendas_clientes[vendas_clientes['order_purchase_timestamp'].between(INICIO, FIM)
                                  & ~vendas_clientes['order_status'].isin(['canceled', 'unavailable'])].copy()
vendas_clientes['dia_compra'] = vendas_clientes['order_purchase_timestamp'].dt.date
dias_por_cliente = vendas_clientes.groupby('customer_unique_id')['dia_compra'].nunique()
primeiro = (vendas_clientes.sort_values('order_purchase_timestamp')
                           .drop_duplicates(subset='customer_unique_id', keep='first')
                           .merge(nota_pedido[['order_id', 'review_score']], on='order_id', how='left'))
primeiro['voltou'] = primeiro['customer_unique_id'].map(dias_por_cliente) > 1
com_tempo = primeiro[primeiro['order_purchase_timestamp'] < '2018-03-01'].copy()
com_tempo['grupo_nota'] = pd.cut(com_tempo['review_score'], bins=[0, 2, 3, 5], labels=['Nota 1 e 2', 'Nota 3', 'Nota 4 e 5'])
recompra = com_tempo.groupby('grupo_nota', observed=True)['voltou'].agg(clientes='size', pct_recompra='mean')
recompra['pct_compra_unica'] = 1 - recompra['pct_recompra']
grava(recompra.reset_index().round(4), 't_recompra_por_nota')

# achado 8: etapas da entrega (notebook 04, item 6.5)
limite = items.groupby('order_id')['shipping_limit_date'].max().rename('limite_postagem')
etapas = entregues.merge(limite, on='order_id')
postagem = etapas['order_delivered_carrier_date']
fora_de_ordem = ((postagem < etapas['order_purchase_timestamp']) | (postagem < etapas['order_approved_at'])
                 | (etapas['order_delivered_customer_date'] < postagem))
etapas = etapas[postagem.notna() & ~fora_de_ordem].copy()
etapas['dias_vendedor'] = (etapas['order_delivered_carrier_date'] - etapas['order_purchase_timestamp']).dt.total_seconds() / 86400
etapas['dias_transportadora'] = (etapas['order_delivered_customer_date'] - etapas['order_delivered_carrier_date']).dt.total_seconds() / 86400
etapas['postou_no_prazo'] = etapas['order_delivered_carrier_date'] <= etapas['limite_postagem']
etapas['situacao'] = np.where(etapas['atrasado'], 'Atrasado', 'No prazo')
resumo_etapas = etapas.groupby('situacao').agg(pedidos=('order_id', 'size'),
                                               dias_vendedor_mediana=('dias_vendedor', 'median'),
                                               dias_transportadora_mediana=('dias_transportadora', 'median'),
                                               pct_postou_no_prazo=('postou_no_prazo', 'mean'))
grava(resumo_etapas.reset_index().round(4), 't_etapas_entrega')

# achado 11: saindo de SP, RJ x PR x MG (notebook 04, item 6.4.1)
coord = geolocation.groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].mean()
primeiro_vendedor = items.groupby('order_id')['seller_id'].first()
rotas = entregues.merge(customers[['customer_id', 'customer_zip_code_prefix', 'customer_state']], on='customer_id')
rotas['seller_id'] = rotas['order_id'].map(primeiro_vendedor)
rotas = rotas.merge(sellers[['seller_id', 'seller_zip_code_prefix', 'seller_state']], on='seller_id')
rotas = rotas.join(coord, on='customer_zip_code_prefix').join(coord.add_suffix('_seller'), on='seller_zip_code_prefix')
lat1, lng1 = np.radians(rotas['geolocation_lat']), np.radians(rotas['geolocation_lng'])
lat2, lng2 = np.radians(rotas['geolocation_lat_seller']), np.radians(rotas['geolocation_lng_seller'])
a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lng2 - lng1) / 2) ** 2
rotas['km'] = 6371 * 2 * np.arcsin(np.sqrt(a))
rotas_sp = (rotas[(rotas['seller_state'] == 'SP') & rotas['customer_state'].isin(['RJ', 'PR', 'MG'])]
            .groupby('customer_state').agg(pedidos=('order_id', 'size'), km_mediano=('km', 'median'),
                                           pct_atraso=('atrasado', 'mean')))
grava(rotas_sp.rename_axis('destino').reset_index().round(4), 't_rotas_saindo_de_sp')

# achados 15 a 17: previsão (notebook 05, itens 9.1 a 9.4)
vendas = pedidos[pedidos['no_recorte'] & pedidos['venda_valida']]
mensal = vendas.groupby('mes')['receita'].sum() / 1_000_000
base = mensal.loc['2018-01':'2018-07']
media, menor, maior = base.mean(), base.min(), base.max()
efeito = mensal.loc['2017-11'] / mensal.loc[['2017-10', '2017-12']].mean() - 1
meses = pd.period_range('2017-01', '2018-12', freq='M').astype(str)
previsao = pd.DataFrame({'mes': pd.to_datetime(meses).date})
previsao['realizado_mi'] = [mensal.get(m) for m in meses]
previsao['situacao'] = ['Previsto' if m > '2018-08' else 'Incompleto' if m == '2018-08' else 'Realizado' for m in meses]
futuro = [m >= '2018-08' for m in meses]
previsao['previsto_mi'] = np.where(futuro, media, np.nan)
previsao['faixa_min_mi'] = np.where(futuro, menor, np.nan)
previsao['faixa_max_mi'] = np.where(futuro, maior, np.nan)
previsao['black_friday_mi'] = np.where(np.array(meses) == '2018-11', media * (1 + efeito), np.nan)
grava(previsao.round(3), 't_previsao_mensal')

teste_base = mensal.loc['2018-01':'2018-04']
teste = pd.DataFrame({'mes': pd.to_datetime(['2018-05', '2018-06', '2018-07']).date,
                      'previsto_mi': teste_base.mean(),
                      'real_mi': mensal.loc['2018-05':'2018-07'].values})
teste['erro_pct'] = teste['real_mi'] / teste['previsto_mi'] - 1
teste['dentro_da_faixa'] = teste['real_mi'].between(teste_base.min(), teste_base.max())
grava(teste.round(4), 't_teste_previsao')

# valores esperados das medidas DAX, calculados com as mesmas regras sobre fato_pedidos
f = fato
v = f[f['venda_valida']]
e = f[f['entregue']]
valor_mes = v.groupby('mes')['valor_vendido'].sum()
mes = lambda texto: pd.Timestamp(texto).date()
jan_jul = lambda ano: valor_mes[(valor_mes.index >= mes(f'{ano}-01-01')) & (valor_mes.index <= mes(f'{ano}-07-01'))].sum()
dias = v.groupby('cliente')['data_compra'].nunique()
nordeste = populacao.loc[populacao['regiao'] == 'Nordeste', 'uf']
rj = e[e['uf_cliente'] == 'RJ']
conferencia = [
    ('.valor_vendido', v['valor_vendido'].sum(), 'R$ 15,68 mi', 'notebook 02, item 2.6'),
    ('.pedidos_vendidos', len(v), '97.905', 'notebook 05, item 8.1'),
    ('.ticket_mediano', v['valor_vendido'].median(), 'cerca de R$ 105', 'notebook 02, item 2.7'),
    ('.pedidos_entregues', len(e), '96.203', 'notebook 03, item 4.5'),
    ('.pedidos_atrasados', int(e['atrasado'].sum()), '6.531', 'notebook 03, item 4.5'),
    ('.pct_atraso', e['atrasado'].mean(), '6,8%', 'notebook 03, item 4.5'),
    ('.prazo_mediano_dias', e['dias_entrega'].median(), '10,2 dias', 'notebook 03, item 4.5'),
    ('.nota_media (entregues no prazo)', e.loc[e['atrasado'] == False, 'nota'].mean(), '4,3', 'notebook 03'),
    ('.nota_media (entregues atrasados)', e.loc[e['atrasado'] == True, 'nota'].mean(), '2,3', 'notebook 03'),
    ('.pct_notas_1_2 (no prazo)', (e.loc[e['atrasado'] == False, 'nota'] <= 2).mean(), '9%', 'notebook 03, item 4.6'),
    ('.pct_notas_1_2 (atrasados)', (e.loc[e['atrasado'] == True, 'nota'] <= 2).mean(), '61%', 'notebook 03, item 4.6'),
    ('.pct_recompra', (dias > 1).mean(), '2,2%', 'notebook 03, item 5.2'),
    ('.parte_dos_atrasos (RJ)', rj['atrasado'].sum() / e['atrasado'].sum(), '23%', 'notebook 04, item 6.4'),
    ('.pct_atraso (RJ)', rj['atrasado'].mean(), '12,1%', 'notebook 04, item 6.4'),
    ('.pct_moradores (Nordeste)', populacao.loc[populacao['regiao'] == 'Nordeste', 'populacao_2018'].sum() / populacao['populacao_2018'].sum(), '27%', 'notebook 05, item 8.2'),
    ('.pct_pedidos (Nordeste)', v['uf_cliente'].isin(nordeste).mean(), '9,5%', 'notebook 05, item 8.2'),
    ('.pedidos_100mil_moradores (Nordeste)', v['uf_cliente'].isin(nordeste).sum() / populacao.loc[populacao['regiao'] == 'Nordeste', 'populacao_2018'].sum() * 100_000, '16', 'notebook 05, item 8.2'),
    ('.pct_atraso (Nordeste)', e.loc[e['uf_cliente'].isin(nordeste), 'atrasado'].mean(), '12,8%', 'notebook 05, item 8.2'),
    ('.crescimento_jan_jul', jan_jul(2018) / jan_jul(2017) - 1, '161%', 'notebook 05, item 9.2'),
    ('.efeito_black_friday', valor_mes[mes('2017-11-01')] / ((valor_mes[mes('2017-10-01')] + valor_mes[mes('2017-12-01')]) / 2) - 1, '+44%', 'notebook 05, item 9.4'),
    ('.media_mensal_2018', jan_jul(2018) / 7, 'R$ 1,09 mi', 'notebook 05, item 9.3'),
]
conferencia = pd.DataFrame(conferencia, columns=['medida', 'valor_calculado', 'valor_no_notebook', 'onde_conferir'])
conferencia['valor_calculado'] = conferencia['valor_calculado'].astype(float).round(4)
grava(conferencia, 'conferencia_kpis')
print(conferencia.to_string(index=False))
