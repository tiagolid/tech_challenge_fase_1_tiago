let
    Fonte = Csv.Document(File.Contents(PastaDados & "fato_pedidos.csv"), [Delimiter = ",", Columns = 19, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"pedido", type text}, {"cliente", type text}, {"status", type text}, {"data_compra", type date}, {"mes", type date}, {"venda_valida", type logical}, {"entregue", type logical}, {"atrasado", type logical}, {"uf_cliente", type text}, {"uf_vendedor", type text}, {"categoria", type text}, {"meio_pagamento", type text}, {"parcelas", Int64.Type}, {"valor_produtos", type number}, {"valor_frete", type number}, {"valor_vendido", type number}, {"nota", Int64.Type}, {"dias_entrega", type number}, {"dias_vs_prometido", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
