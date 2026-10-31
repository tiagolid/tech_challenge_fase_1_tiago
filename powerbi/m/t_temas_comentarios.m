let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_temas_comentarios.csv"), [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"nota", Int64.Type}, {"posicao", Int64.Type}, {"tema", type text}, {"parcela_estimada", type text}, {"parcela_aprox", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
