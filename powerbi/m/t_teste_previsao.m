let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_teste_previsao.csv"), [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"mes", type date}, {"previsto_mi", type number}, {"real_mi", type number}, {"erro_pct", type number}, {"dentro_da_faixa", type logical}}, "en-US")
in
    #"Tipo Alterado com Localidade"
