let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_previsao_mensal.csv"), [Delimiter = ",", Columns = 7, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"mes", type date}, {"realizado_mi", type number}, {"situacao", type text}, {"previsto_mi", type number}, {"faixa_min_mi", type number}, {"faixa_max_mi", type number}, {"black_friday_mi", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
