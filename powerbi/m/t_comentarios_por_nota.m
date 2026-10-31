let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_comentarios_por_nota.csv"), [Delimiter = ",", Columns = 3, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"nota", Int64.Type}, {"avaliacoes", Int64.Type}, {"pct_com_comentario", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
