# Relatório no Power BI

O relatório executivo é montado no Power BI a partir das tabelas geradas por `scripts/exporta_powerbi.py`, com as mesmas regras dos notebooks.

Versão publicada: [link público](https://app.powerbi.com/view?r=eyJrIjoiMThjMzFjYmItYTJhMi00NDhjLTg3MzAtZTI5Mzg0NmViNGYzIiwidCI6Ijk4YTNmZjI0LTI0NDgtNDk3Zi1hZjJkLTFiZThjZjlmMGM2OCJ9). Cópia em PDF: `Olist_Tech_Challenge.pdf`.

## Como montar

1. Gere as tabelas: `python scripts/exporta_powerbi.py` (grava em `data/powerbi/`).
2. No Power BI, crie o parâmetro `PastaDados` com o conteúdo de `m/PastaDados.m` (ajuste o caminho da pasta `data/powerbi/` do seu computador, terminando com `\`).
3. Para cada arquivo de `m/`, crie uma consulta nula com o mesmo nome do arquivo e cole o código no Editor Avançado.
4. Relacionamento: `dim_estado[uf]` (1) para `fato_pedidos[uf_cliente]` (muitos). As tabelas `t_` ficam soltas.
5. Crie as colunas de `dax/colunas_fato_pedidos.dax` na tabela `fato_pedidos` e as medidas de `dax/medidas.dax`.
6. Classifique `faixa_atraso` pela coluna `faixa_atraso_ordem`.
7. Confira os cartões com `conferencia_kpis`: cada medida tem o valor esperado e o item do notebook de onde ele vem.

## Formatos

- Medidas e colunas que começam com `pct_` são frações: formate como porcentagem.
- Colunas terminadas em `_mi` estão em milhões de reais.

## Páginas

| Página | Conteúdo | Achados (`docs/para_apresentacao.md`) |
|---|---|---|
| 1. Sumário | valor vendido, pedidos, % de atraso, nota média, recompra e a história em três frases | |
| 2. Contexto | a Olist, a base, o período e os limites dos dados | 1, 2 |
| 3. Vendas | valor vendido por mês, formas de pagamento, categorias | 3, 7, 15 |
| 4. Entrega e nota | nota no prazo x atrasado, avaliação antes de receber, comentários, recompra | 4, 5, 9, 10 |
| 5. Onde atrasa | atraso por estado, RJ x PR x MG, etapas da entrega | 6, 8, 11 |
| 6. Espaço para crescer | Nordeste: moradores x pedidos | 12, 13, 14 |
| 7. Próximos meses | previsão e Black Friday | 16, 17 |
| 8. Conclusões | recomendações (`docs/recomendacoes.md`) | |
