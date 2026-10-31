let
    Fonte = Csv.Document(File.Contents(PastaDados & "conferencia_kpis.csv"), [Delimiter = ",", Columns = 4, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"medida", type text}, {"valor_calculado", type number}, {"valor_no_notebook", type text}, {"onde_conferir", type text}}, "en-US")
in
    #"Tipo Alterado com Localidade"
