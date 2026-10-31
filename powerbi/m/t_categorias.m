let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_categorias.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"categoria", type text}, {"valor_vendido", type number}, {"pct_valor_vendido", type number}, {"posicao", Int64.Type}}, "en-US")
in
    #"Tipo Alterado com Localidade"
