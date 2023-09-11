from notasnegociacao.notanegociacao import NotaNegociacao
from typing import List
import os
import pdfplumber


class Corretora:
    notasNegociacao: List[NotaNegociacao]

    def __init__(self, dir: str = None):
        if (dir != None):
            self.notasNegociacao = self.lerNotasDiretorio(dir)

    def lerNotasDiretorio(self, dir: str) -> List[NotaNegociacao]:
        result: List[NotaNegociacao] = []

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

        return result
