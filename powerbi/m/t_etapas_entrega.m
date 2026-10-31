let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_etapas_entrega.csv"), [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"situacao", type text}, {"pedidos", Int64.Type}, {"dias_vendedor_mediana", type number}, {"dias_transportadora_mediana", type number}, {"pct_postou_no_prazo", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
