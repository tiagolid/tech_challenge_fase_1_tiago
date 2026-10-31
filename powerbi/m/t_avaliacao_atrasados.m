let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_avaliacao_atrasados.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"momento", type text}, {"pedidos", Int64.Type}, {"pct_notas_1_2", type number}, {"pct_dos_atrasados", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
