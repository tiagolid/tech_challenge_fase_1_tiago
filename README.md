# Tech Challenge Fase 1 · Olist

Relatório executivo para investidores sobre o marketplace Olist (Brazilian E-Commerce Public Dataset, ~100 mil pedidos, 2016 a 2018). Pós-Tech Data Analytics FIAP.

**Pergunta central:** a Olist cresce, mas o atraso na entrega derruba a nota e a nota baixa reduz a recompra? Onde investir para corrigir?

## Como reproduzir

1. Python 3.12 e as bibliotecas de `requirements.txt` (`pip install -r requirements.txt`).
2. Baixe a base para `data/raw/`:
   ```python
   import kagglehub, shutil, glob
   p = kagglehub.dataset_download('olistbr/brazilian-ecommerce')
   for f in glob.glob(p + '/*.csv'): shutil.copy(f, 'data/raw/')
   ```
3. A população por estado do IBGE já vem no repositório, em `data/external/` (fonte em `docs/fontes_externas.md`).
4. Rode os notebooks em ordem.
5. Para o relatório no Power BI, rode `scripts/exporta_powerbi.py` e siga `powerbi/README.md`. O `01` gera `data/processed/pedidos.csv`, que os demais usam.

## Fluxo de dados (ETL)

```
Kaggle (9 CSVs) ──► data/raw/ ──► notebook 01 ──► data/processed/pedidos.csv ──► notebooks 02+ ──► relatório
   Extração          bruto,        validação +       1 linha por pedido,           análises
                     intocado      transformação     31 colunas
```

1. **Extração:** `kagglehub` baixa a versão 2 da base pública para `data/raw/`. Os arquivos brutos nunca são alterados.
2. **Validação:** volume, nulos, duplicatas, chaves únicas, granularidade, órfãos e período de cada tabela.
3. **Transformação:** cada tabela fato é resumida para uma linha por pedido e só então é juntada a `orders` (left join). As colunas calculadas (prazo, atraso, valor vendido, recorte) seguem as regras abaixo.
4. **Conferência:** a base final precisa ter o mesmo número de linhas de `orders` (99.441).
5. **Carga:** `data/processed/pedidos.csv`, consumida pelos notebooks de análise.

## Notebooks

| # | Notebook | Conteúdo |
|---|---|---|
| 01 | `01_validacao_dados_brutos.ipynb` | Validação da tabela de pedidos: hipóteses, testes, decisões de limpeza e recorte do período |
| 02 | `02_itens_e_pagamentos.ipynb` | A Olist cresce em valor vendido, e esse valor é confiável? (itens e pagamentos) |
| 03 | `03_avaliacoes_e_clientes.ipynb` | O atraso derruba a nota, e a nota baixa reduz a recompra? (avaliações e clientes) |
| 04 | `04_vendedores_e_produtos.ipynb` | Onde estão os atrasos e as notas ruins: rotas, vendedores e produtos? |
| 05 | `05_espaco_para_crescer_e_previsao.ipynb` | Onde ainda há espaço para crescer e o que esperar dos próximos meses? (população do IBGE) |

## Regras de dados (governança)

| Problema | Decisão |
|---|---|
| Itens e pagamentos multiplicam linhas ao juntar (+27% no total pago) | Resumir cada tabela por pedido antes de juntar |
| Pontas do período quase vazias | Recorte de jan/2017 a ago/2018 |
| `customer_id` muda a cada pedido | Cliente = `customer_unique_id` |
| `geolocation` com ~53 linhas por CEP | Coordenada média por CEP. A distância em km foi testada (notebook 04, item 6.4.1) e não muda nenhuma conclusão: o relatório usa o estado |
| Pedido com mais de uma avaliação | Última avaliação respondida |
| Valor vendido (GMV) | Preço + frete dos itens, sem pedidos cancelados ou indisponíveis. Receita e lucro da Olist não estão na base (comissão de 19% a 21% segundo o NeoFeed, 2021) |
| Prazo e atraso | Só pedidos entregues, comparando dia com dia com a data prometida |

## Fontes externas

Reportagens e documentos usados como contexto (modelo de cobrança da Olist, fluxo do pedido, Black Friday 2017) estão em [`docs/fontes_externas.md`](docs/fontes_externas.md).
