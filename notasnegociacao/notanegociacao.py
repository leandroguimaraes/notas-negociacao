
from notasnegociacao.negociorealizado import NegocioRealizado
from notasnegociacao.resumofinanceiro import ResumoFinanceiro
from notasnegociacao.resumonegocios import ResumoNegocios
from notasnegociacao.util import strToFloat
from typing import List
import datetime


class NotaNegociacao:
    numero: str
    dataPregao: datetime.date
    cliente: str
    codigoCliente: str
    negociosRealizados: List[NegocioRealizado]
    resumoNegocios: ResumoNegocios
    resumoFinanceiro: ResumoFinanceiro

    def __init__(self, numero: str = None):
        self.numero = numero

        self.resumoNegocios = ResumoNegocios()
        self.resumoFinanceiro = ResumoFinanceiro()

    @staticmethod
    def parseText(text: str, notas=[]):
        nota: NotaNegociacao = None
        folhaAtual = 0

        nNegocios = 0
        isOpcao = False
        lines = text.splitlines()

        i = 0
        while (i < len(lines)):
            if (lines[i] == 'Nr. nota'):
                nNegocios = 0

                i += 2
                nota = next(
                    (nota for nota in notas if nota.numero == lines[i]), None)
                if (nota == None):
                    nota = NotaNegociacao(lines[i])
                    notas.append(nota)

            if (lines[i] == 'Folha'):
                i += 2
                folhaAtual = lines[i]

            if (lines[i] == 'Data pregão'):
                i += 2
                nota.dataPregao = datetime.datetime.strptime(
                    lines[i], '%d/%m/%Y').date()

            if (lines[i] == 'Cliente'):
                i += 1
                nota.cliente = lines[i]

            if (lines[i] == 'Código cliente'):
                i += 2
                nota.codigoCliente = lines[i]

            if (lines[i] == 'Q Negociação'):
                i += 1
                nota.negociosRealizados = []
                while (lines[i] != ''):
                    nNegocios += 1

                    negocioRealizado = NegocioRealizado()
                    negocioRealizado.negociacao = lines[i]

                    nota.negociosRealizados.append(negocioRealizado)
                    i += 1

            if (lines[i] == 'C/V Tipo mercado'):
                i += 1
                for j in range(nNegocios):
                    nota.negociosRealizados[j].folha = int(folhaAtual)
                    nota.negociosRealizados[j].compraVenda = lines[i][:1]
                    nota.negociosRealizados[j].tipoMercado = lines[i][1:]
                    if 'OPCAO' in nota.negociosRealizados[j].tipoMercado:
                        isOpcao = True
                    else:
                        isOpcao = False

                    i += 1

            if (lines[i] == 'Prazo Especificação do título'):
                if (isOpcao == False):
                    while (lines[i] != 'Preço / Ajuste'):
                        i += 1

                    i += 2
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].especificacaoTitulo = lines[i]

                        i += 1

                    i += 1
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].quantidade = lines[i].replace(
                            '.', '')

                        i += 1

                    i += 1
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].precoAjuste = lines[i].replace(
                            ',', '.')

                        i += 1
                else:
                    i += 1
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].prazo = lines[i][:5]
                        nota.negociosRealizados[j].especificacaoTitulo = lines[i][6:]

                        i += 1

                    while (lines[i] != 'Preço / Ajuste'):
                        i += 1

                    i += 2
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].quantidade = lines[i].replace(
                            '.', '')

                        i += 1

                    i += 1
                    for j in range(nNegocios):
                        nota.negociosRealizados[j].precoAjuste = strToFloat(
                            lines[i])

            if (lines[i] == 'D/C'):
                i += 1
                for j in range(nNegocios):
                    nota.negociosRealizados[j].valorOperacaoAjuste = strToFloat(
                        lines[i][:len(lines[i]) - 3])
                    nota.negociosRealizados[j].debitoCredito = lines[i][len(
                        lines[i]) - 1]

                    i += 1

            if (lines[i] == 'A coluna Q indica liquidação no Agente do Qualificado.'):
                i += 2
                nota.resumoNegocios.debentures = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.vendasVista = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.comprasVista = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.opcoesCompras = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.opcoesVendas = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.operacoesTermo = strToFloat(lines[i])
                i += 1
                nota.resumoNegocios.valorOperacoesTitulosPublicosVNom = strToFloat(
                    lines[i])
                i += 1
                nota.resumoNegocios.valorOperacoes = strToFloat(lines[i])
                i += 1

            if ('I.R.R.F. s/ operações' in lines[i]):
                nota.resumoFinanceiro.custosOperacionais.irrfSOperacoesBase = strToFloat(
                    lines[i][lines[i].index('R$') + 2:])

            if ('Outros' in lines[i]):
                i += 2
                nota.resumoFinanceiro.clearing.valorLiquidoOperacoes = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.clearing.taxaLiquidacao = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.clearing.taxaRegistro = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.clearing.totalCBLC = strToFloat(lines[i])

                i += 2
                nota.resumoFinanceiro.bolsa.taxaTermoOpcoes = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.bolsa.taxaANA = strToFloat(lines[i])
                i += 1
                nota.resumoFinanceiro.bolsa.emolumentos = strToFloat(lines[i])
                i += 1
                nota.resumoFinanceiro.bolsa.totalBovespaSoma = strToFloat(
                    lines[i])

                i += 2
                nota.resumoFinanceiro.custosOperacionais.taxaOperacional = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.execucao = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.taxaCustodia = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.impostos = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.irrfSOperacoes = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.outros = strToFloat(
                    lines[i])

            if ('Líquido para' in lines[i]):
                nota.resumoFinanceiro.custosOperacionais.liquidoParaData = datetime.datetime.strptime(
                    lines[i][-10:], '%d/%m/%Y').date()

                i += 3
                nota.resumoFinanceiro.custosOperacionais.totalCustosDespesas = strToFloat(
                    lines[i])
                i += 1
                nota.resumoFinanceiro.custosOperacionais.liquidoParaDataValor = strToFloat(
                    lines[i])

            if (lines[i] == 'C' or lines[i] == 'D'):
                print(f'line: {i}')
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.clearing.valorLiquidoOperacoes *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.clearing.taxaLiquidacao *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.clearing.taxaRegistro *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.clearing.totalCBLC *= -1

                i += 2
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.bolsa.taxaTermoOpcoes *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.bolsa.taxaANA *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.bolsa.emolumentos *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.bolsa.totalBovespaSoma *= -1

                i += 2
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.taxaOperacional *= -1

                i += 2
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.outros *= -1

                i += 2
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.totalCustosDespesas *= -1

                i += 1
                if (lines[i] == 'D'):
                    nota.resumoFinanceiro.custosOperacionais.liquidoParaDataValor *= -1

            i += 1

        return notas
