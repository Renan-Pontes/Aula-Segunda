"""
Importa o CSV de taxas de juros do Banco Central (BCB) para o modelo CalculosDeJuros.

Uso:
    python manage.py import_bcb_csv                      # importa data/bcb_taxas_juros_*.csv
    python manage.py import_bcb_csv caminho/arquivo.csv  # importa um arquivo específico
    python manage.py import_bcb_csv --limpar             # apaga os registros antes de importar
"""
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import CalculosDeJuros

DATA_DIR = Path(settings.BASE_DIR) / "data"

# coluna do CSV -> campo do modelo
COLUNAS = {
    "InicioPeriodo": "InicioPeriodo",
    "FimPeriodo": "FimPeriodo",
    "codigoSegmento": "CodigoSegmento",
    "Segmento": "Segmento",
    "codigoModalidade": "CodigoModalidade",
    "Modalidade": "Modalidade",
    "Posicao": "Posicao",
    "InstituicaoFinanceira": "InstituicaoFinanceira",
    "cnpj8": "CNPJ8",
    "TaxaJurosAoMes": "TaxaJurosAoMes",
    "TaxaJurosAoAno": "TaxaJurosAoAno",
}
DECIMAIS = {"TaxaJurosAoMes", "TaxaJurosAoAno"}


class Command(BaseCommand):
    help = "Importa um CSV de taxas de juros do BCB para a tabela CalculosDeJuros."

    def add_arguments(self, parser):
        parser.add_argument(
            "arquivo",
            nargs="?",
            help="Caminho do CSV. Padrão: o CSV mais recente em backend/data/.",
        )
        parser.add_argument(
            "--limpar",
            action="store_true",
            help="Apaga todos os registros de CalculosDeJuros antes de importar.",
        )

    def handle(self, *args, **options):
        caminho = self._resolver_arquivo(options["arquivo"])
        registros = list(self._ler_csv(caminho))

        with transaction.atomic():
            if options["limpar"]:
                apagados, _ = CalculosDeJuros.objects.all().delete()
                self.stdout.write(f"Apagados {apagados} registros existentes.")
            # bulk_create não chama save(), então os valores do CSV são gravados como estão.
            CalculosDeJuros.objects.bulk_create(registros, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(f"Importados {len(registros)} registros de {caminho.name}.")
        )

    def _resolver_arquivo(self, arquivo):
        if arquivo:
            caminho = Path(arquivo)
        else:
            candidatos = sorted(DATA_DIR.glob("bcb_taxas_juros_*.csv"))
            if not candidatos:
                raise CommandError(f"Nenhum CSV bcb_taxas_juros_*.csv encontrado em {DATA_DIR}.")
            caminho = candidatos[-1]
        if not caminho.is_file():
            raise CommandError(f"Arquivo não encontrado: {caminho}")
        return caminho

    def _ler_csv(self, caminho):
        with caminho.open(encoding="utf-8", newline="") as f:
            leitor = csv.DictReader(f)
            faltando = set(COLUNAS) - set(leitor.fieldnames or [])
            if faltando:
                raise CommandError(f"Colunas ausentes no CSV: {', '.join(sorted(faltando))}")

            for numero, linha in enumerate(leitor, start=2):
                campos = {}
                for coluna, campo in COLUNAS.items():
                    valor = (linha[coluna] or "").strip()
                    if campo in DECIMAIS:
                        try:
                            valor = Decimal(valor)
                        except InvalidOperation:
                            raise CommandError(
                                f"Linha {numero}: valor inválido em {coluna}: {valor!r}"
                            )
                    campos[campo] = valor
                yield CalculosDeJuros(**campos)
