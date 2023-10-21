from notasnegociacao.notanegociacao import NotaNegociacao
import os
import pdfplumber


class Corretora:
    notasNegociacao: list[NotaNegociacao]

    def __init__(self, dir: str = None):
        if (dir != None):
            self.notasNegociacao = self.lerNotasDiretorio(dir)

    def lerNotasDiretorio(self, dir: str) -> list[NotaNegociacao]:
        result: list[NotaNegociacao] = []

        notasPdf = [f for f in os.listdir(dir) if f.endswith('.pdf')]

        pdfCount = 1
        for pdf in notasPdf:
            with pdfplumber.open(dir + pdf) as pdfFile:
                print(f'Processando PDFs: {pdfCount}/{len(notasPdf)}')
                print(pdf)
                pdfCount += 1

                for page in pdfFile.pages:
                    result = NotaNegociacao.parseText(
                        page.extract_text(), result)

        return sorted(result, key=lambda r: r.dataPregao)
