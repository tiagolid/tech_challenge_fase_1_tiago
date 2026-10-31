let
    Fonte = Csv.Document(File.Contents(PastaDados & "t_pagamentos.csv"), [Delimiter = ",", Columns = 3, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {{"forma_pagamento", type text}, {"pct_pagamentos", type number}, {"parcelas_mediana", type number}}, "en-US")
in
    #"Tipo Alterado com Localidade"
