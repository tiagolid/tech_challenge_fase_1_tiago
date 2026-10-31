let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_recompra_por_nota.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"grupo_nota", type text}, {"clientes", Int64.Type}, {"pct_recompra", type number}, {"pct_compra_unica", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
