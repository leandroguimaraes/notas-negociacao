import datetime


class ResumoFinanceiroClearing:
    valorLiquidoOperacoes: float
    taxaLiquidacao: float
    taxaRegistro: float
    totalCBLC: float


class ResumoFinanceiroBolsa:
    taxaTermoOpcoes: float
    taxaANA: float
    emolumentos: float
    totalBovespaSoma: float


class ResumoFinanceiroCustosOperacionais:
    taxaOperacional: float
    execucao: float
    taxaCustodia: float
    impostos: float
    irrfSOperacoesBase: float
    irrfSOperacoes: float
    irrfDayTradeBase: float
    irrfDayTradeProjecao: float
    outros: float
    totalCustosDespesas: float


class ResumoFinanceiro:
    clearing: ResumoFinanceiroClearing
    bolsa: ResumoFinanceiroBolsa
    custosOperacionais: ResumoFinanceiroCustosOperacionais
    liquidoParaData: datetime.date
    liquidoParaDataValor: float

    def __init__(self):
        self.clearing = ResumoFinanceiroClearing()
        self.bolsa = ResumoFinanceiroBolsa()
        self.custosOperacionais = ResumoFinanceiroCustosOperacionais()
