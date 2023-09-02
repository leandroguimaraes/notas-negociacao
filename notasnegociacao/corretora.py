from notasnegociacao.notanegociacao import NotaNegociacao
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from typing import List
import io
import os


class Corretora:
    def __init__(self, dir: str = None):
        if (dir != None):
            self.lerNotasDiretorio(dir)

    def lerNotasDiretorio(self, dir: str):
        return self.lerNotasDiretorio(dir)

    def lerNotasDiretorio(self, dir: str):
        result: List[NotaNegociacao] = []

        notas_pdf = [f for f in os.listdir(dir) if f.endswith('.pdf')]

        pdfCount = 1
        for pdf in notas_pdf:
            with open(dir + pdf, "rb") as pdf_file:
                print(f'Processando PDFs: {pdfCount}/{len(notas_pdf)}')
                print(pdf)
                pdfCount += 1

                output_buffer = io.StringIO()
                extract_text_to_fp(pdf_file, output_buffer,
                                   laparams=LAParams())
                text = output_buffer.getvalue()

                result = NotaNegociacao.parseText(text, result)

                output_buffer.close()

        return result
