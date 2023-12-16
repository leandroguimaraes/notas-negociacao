
from notasnegociacao.negociorealizado import NegocioRealizado
from notasnegociacao.resumofinanceiro import ResumoFinanceiro
from notasnegociacao.resumonegocios import ResumoNegocios
from notasnegociacao.util import strToFloat, strToInt
import datetime


class NotaNegociacao:
    numero: str
    dataPregao: datetime.date
    negociosRealizados: list[NegocioRealizado]
    resumoNegocios: ResumoNegocios
    resumoFinanceiro: ResumoFinanceiro

    OBS = [
        '2',  # Corretora ou pessoa vinculada atuou na contra parte
        '#',  # Negócio direto
        '8',  # Liquidação Institucional
        'D',  # Day Trade
        'F',  # Cobertura
        'B',  # Debêntures
        'A',  # Posição futuro
        'C',  # Clubes e fundos de Ações
        'P',  # Carteira Própria
        'H',  # Home Broker
        'X',  # Box
        'Y',  # Desmanche de Box
        'L',  # Precatório
        'T',  # Liquidação pelo Bruto
        'I',  # POP
    ]

    def __init__(self, numero: str = None):
        self.numero = numero

        self.negociosRealizados = []
        self.resumoNegocios = ResumoNegocios()
        self.resumoFinanceiro = ResumoFinanceiro()

    @staticmethod
    def parseText(text: str, notas: list['NotaNegociacao'] = []) -> list['NotaNegociacao']:
        nota: NotaNegociacao = None
        folhaAtual = 0

        lines = text.splitlines()

        i = 0
        while (i < len(lines)):
            if ('Nr. nota' in lines[i]):
                i += 1
                line = lines[i].split()
                folhaAtual = strToInt(line[1])

                nota = next(
                    (nota for nota in notas if nota.numero == line[0]), None)

                if (nota == None):
                    nota = NotaNegociacao(line[0])
                    notas.append(nota)

                nota.dataPregao = datetime.datetime.strptime(
                    line[2], '%d/%m/%Y').date()

            if (lines[i] == 'Negócios realizados'):
                i += 2

                while ('Resumo dos Negócios' not in lines[i]):
                    nota.negociosRealizados.append(NotaNegociacao.getNegocioInfo(
                        lines[i], folhaAtual))

                    i += 1

                # verifica se a listagem de operações continua em outra folha
                j = i
                while ('Total Bovespa' not in lines[j]):
                    j += 1

                if ('CONTINUA' in lines[j]):
                    break

            if ('Clearing' in lines[i]):
                nota.resumoNegocios.debentures = strToFloat(lines[i][lines[i].find(
                    ' ') + 1:lines[i].rfind(' ')])

            if ('Vendas à vista' in lines[i]):
                lines[i] = lines[i].replace('Vendas à vista ', '')
                nota.resumoNegocios.vendasVista = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.clearing.valorLiquidoOperacoes = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.clearing.valorLiquidoOperacoes *= -1

            if ('Compras à vista' in lines[i]):
                lines[i] = lines[i].replace('Compras à vista ', '')
                nota.resumoNegocios.comprasVista = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.clearing.taxaLiquidacao = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.clearing.taxaLiquidacao *= -1

            if ('Opções - compras' in lines[i]):
                lines[i] = lines[i].replace('Opções - compras ', '')
                nota.resumoNegocios.opcoesCompras = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.clearing.taxaRegistro = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.clearing.taxaRegistro *= -1

            if ('Opções - vendas' in lines[i]):
                lines[i] = lines[i].replace('Opções - vendas ', '')
                nota.resumoNegocios.opcoesVendas = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.clearing.totalCBLC = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.clearing.totalCBLC *= -1

            if ('Operações à termo' in lines[i]):
                lines[i] = lines[i].replace('Operações à termo ', '')
                nota.resumoNegocios.operacoesTermo = strToFloat(
                    lines[i][:lines[i].find(' ')])

            if ('Valor das oper. c/ títulos públ. (v. nom.)' in lines[i]):
                lines[i] = lines[i].replace(
                    'Valor das oper. c/ títulos públ. (v. nom.) ', '')
                nota.resumoNegocios.valorOperacoesTitulosPublicosVNom = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.bolsa.taxaTermoOpcoes = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.bolsa.taxaTermoOpcoes *= -1

            if ('Valor das operações' in lines[i]):
                lines[i] = lines[i].replace(
                    'Valor das operações ', '')
                nota.resumoNegocios.valorOperacoes = strToFloat(
                    lines[i][:lines[i].find(' ')])

                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.bolsa.taxaANA = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.bolsa.taxaANA *= -1

            if ('Emolumentos' in lines[i]):
                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.bolsa.emolumentos = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.bolsa.emolumentos *= -1

            if ('Total Bovespa / Soma' in lines[i]):
                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.bolsa.totalBovespaSoma = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.bolsa.totalBovespaSoma *= -1

            if ('Taxa Operacional' in lines[i]):
                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                nota.resumoFinanceiro.custosOperacionais.taxaOperacional = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.taxaOperacional *= -1

            if ('Execução' in lines[i]):
                nota.resumoFinanceiro.custosOperacionais.execucao = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:]) * -1

            if ('Taxa de Custódia' in lines[i]):
                nota.resumoFinanceiro.custosOperacionais.taxaCustodia = strToFloat(
                    lines[i][lines[i].rfind(' ') + 1:]) * -1

            if ('Impostos' in lines[i]):
                lineInfo = lines[i].split()
                nota.resumoFinanceiro.custosOperacionais.impostos = strToFloat(
                    lineInfo[1]) * -1

            if ('I.R.R.F. s/ operações' in lines[i]):
                lineInfo = lines[i][lines[i].find('R$') + 2:].split()
                nota.resumoFinanceiro.custosOperacionais.irrfSOperacoesBase = strToFloat(
                    lineInfo[0])

                nota.resumoFinanceiro.custosOperacionais.irrfSOperacoes = strToFloat(
                    lineInfo[1])

                nota.resumoFinanceiro.custosOperacionais.irrfSOperacoes *= -1

            if ('IRRF Day Trade' in lines[i]):
                lines[i] = lines[i][lines[i].find('R$') + 3:]
                nota.resumoFinanceiro.custosOperacionais.irrfDayTradeBase = strToFloat(
                    lines[i][:lines[i].find(' ')]) * -1

                lines[i] = lines[i][lines[i].find('R$') + 3:]
                nota.resumoFinanceiro.custosOperacionais.irrfDayTradeProjecao = strToFloat(
                    lines[i][:lines[i].find(' ')]) * -1

                lines[i] = lines[i][lines[i].find(' ') + 1:]
                lineInfo = lines[i].split()
                nota.resumoFinanceiro.custosOperacionais.outros = strToFloat(
                    lineInfo[1])

                if (lineInfo[2] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.outros *= -1
            elif ('Outros' in lines[i]):
                lineInfo = lines[i].split()
                nota.resumoFinanceiro.custosOperacionais.outros = strToFloat(
                    lineInfo[1])

                if (lineInfo[2] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.outros *= -1

            if ('Total Custos / Despesas' in lines[i]):
                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                lines[i] = lines[i][lines[i].rfind(' ') + 1:]
                nota.resumoFinanceiro.custosOperacionais.totalCustosDespesas = strToFloat(
                    lines[i])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.totalCustosDespesas *= -1

            if ('Líquido para' in lines[i]):
                creditoDebito = lines[i][-1:]
                lines[i] = lines[i][:lines[i].rfind(' ')]
                lines[i] = lines[i][lines[i].find('/') - 2:]

                lineInfo = lines[i].split()
                nota.resumoFinanceiro.liquidoParaData = datetime.datetime.strptime(
                    lineInfo[0], '%d/%m/%Y').date()

                nota.resumoFinanceiro.liquidoParaDataValor = strToFloat(
                    lineInfo[1])

                if (creditoDebito == 'D'):
                    nota.resumoFinanceiro.liquidoParaDataValor *= -1

                NotaNegociacao.calcResumoFinanceiroNegocio(nota)

            i += 1

        return notas

    @staticmethod
    def getNegocioInfo(line: str, folha: int) -> NegocioRealizado:
        n = NegocioRealizado()
        n.folha = folha

        n.negociacao = line[:line.find(' ')]
        line = line[len(n.negociacao) + 1:]

        n.compraVenda = line[:1]
        line = line[2:]

        n.debitoCredito = line[-1:]
        line = line[:-2]

        n.valorOperacaoAjuste = strToFloat(line[line.rfind(' ') + 1:])
        line = line[:line.rfind(' ')]

        if (n.debitoCredito == 'D'):
            n.valorOperacaoAjuste *= -1

        n.precoAjuste = strToFloat(line[line.rfind(' ') + 1:])
        line = line[:line.rfind(' ')]

        n.quantidade = strToInt(line[line.rfind(' ') + 1:])
        line = line[:line.rfind(' ')]

        obs = ''
        obsLine = line
        while (obsLine[-1:] != ' ' and obsLine[-1:] in NotaNegociacao.OBS):
            obs = obsLine[-1:] + obs
            obsLine = obsLine[:-1]
            if (obsLine[-1:] == ' '):
                line = obsLine[:-1]

        if (obsLine[-1:] == ' '):
            n.obs = obs

        if (line[:5] == 'VISTA'):
            n.tipoMercado = line[:5]
            line = line[6:]

            # algumas notas possuem "Prazo" para vendas à vista
            # o que é um erro e deve ser tratado
            # para estes casos, o "Prazo" é descartado aqui
            if (line[2:3] == '/' and line[5:6] == ' '):
                line = line[6:]
        else:
            n.tipoMercado = line[:line.find('/') - 3]
            line = line[line.find('/') - 2:]

            n.prazo = line[:5]
            line = line[6:]

        n.especificacaoTitulo = line

        return n

    @staticmethod
    def calcResumoFinanceiroNegocio(nota: 'NotaNegociacao'):
        valorLiquidoOperacoes = nota.resumoFinanceiro.clearing.valorLiquidoOperacoes
        for negocio in nota.negociosRealizados:
            perc = abs((negocio.valorOperacaoAjuste /
                       valorLiquidoOperacoes) / 100)

            negocio.resumoFinanceiro.clearing.taxaLiquidacao = nota.resumoFinanceiro.clearing.taxaLiquidacao * perc
            negocio.resumoFinanceiro.clearing.taxaRegistro = nota.resumoFinanceiro.clearing.taxaRegistro * perc
            negocio.resumoFinanceiro.clearing.totalCBLC = \
                negocio.valorOperacaoAjuste + \
                negocio.resumoFinanceiro.clearing.taxaLiquidacao + \
                negocio.resumoFinanceiro.clearing.taxaRegistro

            negocio.resumoFinanceiro.bolsa.taxaTermoOpcoes = nota.resumoFinanceiro.bolsa.taxaTermoOpcoes * perc
            negocio.resumoFinanceiro.bolsa.taxaANA = nota.resumoFinanceiro.bolsa.taxaANA * perc
            negocio.resumoFinanceiro.bolsa.emolumentos = nota.resumoFinanceiro.bolsa.emolumentos * perc
            negocio.resumoFinanceiro.bolsa.totalBovespaSoma = \
                negocio.resumoFinanceiro.bolsa.taxaTermoOpcoes + \
                negocio.resumoFinanceiro.bolsa.taxaANA + \
                negocio.resumoFinanceiro.bolsa.emolumentos

            negocio.resumoFinanceiro.custosOperacionais.taxaOperacional = nota.resumoFinanceiro.custosOperacionais.taxaOperacional * perc
            negocio.resumoFinanceiro.custosOperacionais.execucao = nota.resumoFinanceiro.custosOperacionais.execucao * perc
            negocio.resumoFinanceiro.custosOperacionais.taxaCustodia = nota.resumoFinanceiro.custosOperacionais.taxaCustodia * perc
            negocio.resumoFinanceiro.custosOperacionais.impostos = nota.resumoFinanceiro.custosOperacionais.impostos * perc
            negocio.resumoFinanceiro.custosOperacionais.outros = nota.resumoFinanceiro.custosOperacionais.outros * perc

            negocio.resumoFinanceiro.custosOperacionais.totalCustosDespesas = \
                negocio.resumoFinanceiro.custosOperacionais.taxaOperacional + \
                negocio.resumoFinanceiro.custosOperacionais.execucao + \
                negocio.resumoFinanceiro.custosOperacionais.taxaCustodia + \
                negocio.resumoFinanceiro.custosOperacionais.impostos + \
                negocio.resumoFinanceiro.custosOperacionais.outros

            if hasattr(nota.resumoFinanceiro.custosOperacionais, 'irrfDayTradeProjecao'):
                negocio.resumoFinanceiro.custosOperacionais.irrfDayTradeProjecao = nota.resumoFinanceiro.custosOperacionais.irrfDayTradeProjecao * perc
                negocio.resumoFinanceiro.custosOperacionais.totalCustosDespesas += negocio.resumoFinanceiro.custosOperacionais.irrfDayTradeProjecao

            if hasattr(nota.resumoFinanceiro.custosOperacionais, 'irrfSOperacoes'):
                negocio.resumoFinanceiro.custosOperacionais.irrfSOperacoes = nota.resumoFinanceiro.custosOperacionais.irrfSOperacoes * perc
                negocio.resumoFinanceiro.custosOperacionais.totalCustosDespesas += negocio.resumoFinanceiro.custosOperacionais.irrfSOperacoes
