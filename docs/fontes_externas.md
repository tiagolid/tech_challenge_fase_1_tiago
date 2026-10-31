# Fontes externas

Dados de fora da base Olist usados para contexto. Só a população do IBGE entra em cálculo; as demais servem de comparação e curiosidade no relatório.

## População por estado (IBGE)

| Fonte | O que informa | Onde foi usado |
|---|---|---|
| [IBGE, SIDRA, tabela 6579: população residente estimada, 2018](https://sidra.ibge.gov.br/tabela/6579) | população de cada estado em 2018 (208,5 milhões no total). Baixada pela API (`apisidra.ibge.gov.br/values/t/6579/n3/all/v/all/p/2018`) e salva em `data/external/populacao_uf_2018_ibge.csv` | notebook 05, itens 8.1 a 8.3 (pedidos por 100 mil habitantes) |

## Modelo de negócio da Olist (como a Olist ganha dinheiro)

A base pública não informa a receita da Olist nem o custo da operação. Nenhuma das 9 tabelas traz comissão, mensalidade ou custo: só preço, frete e pagamento do cliente.

| Data | Fonte | O que informa |
|---|---|---|
| 23/10/2019 | [Exame: "Olist, marketplace de marketplaces, recebe R$ 190 mi do SoftBank"](https://exame.com/pme/olist-marketplace-de-marketplaces-recebe-r-190-mi-do-softbank/) | comissão de 20% sobre a venda, taxa de instalação de R$ 450 e mensalidade de R$ 50 a R$ 100; cerca de 7 mil lojistas |
| 19/11/2020 | [Exame: "Olist, marketplace de marketplaces, recebe novos R$ 310 mi do SoftBank"](https://exame.com/pme/olist-marketplace-de-marketplaces-recebe-novos-r-310-mi-do-softbank/) | comissão de 19% a 21% conforme o plano; Pro com mensalidade de R$ 250 e adesão de R$ 499 (19%); Lite sem mensalidade (21%) |
| 15/04/2021 | [NeoFeed: "Olist enche o caixa, capta R$ 144 milhões e traz Goldman Sachs para a lojinha"](https://neofeed.com.br/startups/olist-enche-o-caixa-capta-r-144-milhoes-e-traz-goldman-sachs-para-a-lojinha/) | mensalidade pelo uso da plataforma e comissão de 19% a 21%; 25 mil varejistas |
| sem data | [Brazil Journal: "A Olist matou o negócio que a fez unicórnio"](https://braziljournal.com/a-olist-matou-o-negocio-que-a-fez-unicornio-o-novo-modelo-e-melhor/) | anos depois, a Olist encerrou a intermediação em marketplaces e passou a focar em software (ERP) |

**Ressalva:** a fonte mais próxima do período da base (2017 e 2018) é de out/2019. Não encontrei a tabela de preços de 2017 e 2018 (o arquivo do site no Wayback Machine não pôde ser consultado). As três reportagens coincidem em uma comissão de cerca de 20%, mas o número entra no relatório como **curiosidade**, não como certeza.

## Fluxo do pedido

| Fonte | O que informa | Onde foi usado |
|---|---|---|
| [Olist Developers: Orders](https://dev.olist.com/en/guides-and-tutorials/overview/orders) | fluxo approved → invoice_processing → invoiced → shipped → delivered (documentação atual da API, não a de 2018) | notebook 01, item 1.8 |

## Black Friday 2017

| Data | Fonte | O que informa |
|---|---|---|
| 29/11/2017 | [Mercado & Consumo: "Segundo Ebit, e-commerce faturou R$ 3,2 bilhões da véspera da Black Friday à Cyber Monday"](https://mercadoeconsumo.com.br/29/11/2017/noticias/segundo-ebit-e-commerce-faturou-r-32-bilhoes-da-vespera-da-black-friday-a-cyber-monday/) | Black Friday em 24/11/2017; e-commerce brasileiro faturou R$ 2,1 bilhões no dia (+10,3% sobre 2016); R$ 3,2 bilhões de 23 a 27/11 |
| 27/11/2017 | [Teletime, reportagem sobre o faturamento da Black Friday 2017](https://teletime.com.br/27/11/2017/em-2017-e-commerce-fatura-103-mais-na-black-friday/) | mesmo dado da Ebit |

Usado no notebook 01 (item 1.11) e no notebook 02 (item 2.6): pico de pedidos e de valor vendido em nov/2017.

## Descrição oficial da base

| Fonte | O que informa | Onde foi usado |
|---|---|---|
| [Kaggle: Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (descrição atualizada em 01/10/2021) | "Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments." Também: "Some customers didn't write a review." e os nomes de empresas nos comentários foram trocados por casas de Game of Thrones | notebook 03, itens 4.3 (comentário opcional) e 4.7 (pesquisa na data prometida) |
| mesma página | "Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners." "After a customer purchases the product from Olist Store a seller gets notified to fulfill that order." "Each item might be fulfilled by a distinct seller." | notebook 04: o lojista posta; o transporte é feito por parceiros logísticos da Olist; cada item pode sair de um vendedor diferente |
