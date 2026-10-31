let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_estado.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"uf", type text}, {"estado", type text}, {"regiao", type text}, {"populacao_2018", Int64.Type}}, "en-US")
in
    #"Tipo Alterado com Localidade"
