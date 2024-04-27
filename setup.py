from setuptools import setup, find_packages


setup(
    name="notasnegociacao",
    version="1.0",
    description='Conversão de notas de corretagem em formato PDF para para uma estrutura de objetos Python',
    author='Leandro Martins Guimarães',
    url='https://github.com/leandroguimaraes/notas-negociacao',
    packages=find_packages(),
    install_requires=['pdfplumber']
)
