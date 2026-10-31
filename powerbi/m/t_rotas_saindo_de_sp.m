let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_rotas_saindo_de_sp.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"destino", type text}, {"pedidos", Int64.Type}, {"km_mediano", type number}, {"pct_atraso", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
