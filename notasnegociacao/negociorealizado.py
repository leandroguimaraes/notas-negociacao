from notasnegociacao.resumofinanceiro import ResumoFinanceiro


class NegocioRealizado:
    folha: int
    negociacao: str
    compraVenda: str
    tipoMercado: str
    prazo: str
    especificacaoTitulo: str
    obs: str
    quantidade: int
    precoAjuste: float
    valorOperacaoAjuste: float
    debitoCredito: str
    resumoFinanceiro: ResumoFinanceiro

    def __init__(self):
        self.resumoFinanceiro = ResumoFinanceiro()
