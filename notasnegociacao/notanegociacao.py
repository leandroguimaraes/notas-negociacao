
from notasnegociacao.negociorealizado import NegocioRealizado
from notasnegociacao.resumofinanceiro import ResumoFinanceiro
from notasnegociacao.resumonegocios import ResumoNegocios
from notasnegociacao.util import strToFloat, strToInt
from typing import List
import datetime


class NotaNegociacao:
    numero: str
    dataPregao: datetime.date
    negociosRealizados: List[NegocioRealizado]
    resumoNegocios: ResumoNegocios
    resumoFinanceiro: ResumoFinanceiro

    def __init__(self, numero: str = None):
        self.numero = numero

        self.negociosRealizados = []
        self.resumoNegocios = ResumoNegocios()
        self.resumoFinanceiro = ResumoFinanceiro()

    @staticmethod
    def parseText(text: str, notas=[]):
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

                while (lines[i].find('Resumo dos Negócios') == -1):
                    notas.append(NotaNegociacao.getNegocioInfo(
                        lines[i], folhaAtual))

                    i += 1

            i += 1

        return notas

    @staticmethod
    def getNegocioInfo(line: str, folha: int):
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

        n.precoAjuste = strToFloat(line[line.rfind(' ') + 1:])
        line = line[:line.rfind(' ')]

        n.quantidade = strToInt(line[line.rfind(' ') + 1:])
        line = line[:line.rfind(' ')]

        if (line[-2:-1] == ' '):
            n.obs = line[-1:]
            line = line[:line.rfind(' ')]

        if (line[:5] == 'VISTA'):
            n.tipoMercado = line[:5]
            line = line[6:]
        else:
            n.tipoMercado = line[:line.find('/') - 3]
            line = line[line.find('/') - 2:]

            n.prazo = line[:5]
            line = line[6:]

        n.especificacaoTitulo = line

        return n
