from decimal import Decimal

from django.db import models
#import user
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
     User = models.OneToOneField(User, on_delete=models.CASCADE)
     username = models.CharField(max_length=150, unique=True)
     email = models.EmailField(unique=True)
     password = models.CharField(max_length=128)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     ip_address = models.GenericIPAddressField(null=True, blank=True)
     
     def __str__(self):
          return self.username

class CalculosDeJuros(models.Model):
     InicioPeriodo = models.DateField()
     FimPeriodo = models.DateField()
     CodigoSegmento = models.CharField(max_length=50)
     Segmento = models.CharField(max_length=100)
     CodigoModalidade = models.CharField(max_length=50)
     Modalidade = models.CharField(max_length=100)
     Posicao = models.CharField(max_length=50)
     InstituicaoFinanceira = models.CharField(max_length=100)
     CNPJ8 = models.CharField(max_length=8)
     TaxaJurosAoMes = models.DecimalField(max_digits=10, decimal_places=4)
     TaxaJurosAoAno = models.DecimalField(max_digits=10, decimal_places=4)

     def save(self, *args, **kwargs):
          # TaxaJurosAoAno é derivada de TaxaJurosAoMes. As taxas são percentuais
          # (ex.: 0.2 = 0,2% a.m.), por isso a divisão/multiplicação por 100.
          mes = Decimal(self.TaxaJurosAoMes) / 100
          self.TaxaJurosAoAno = ((1 + mes) ** 12 - 1) * 100
          super().save(*args, **kwargs)

     def __str__(self):
          return f"{self.InicioPeriodo} - {self.FimPeriodo} - {self.Segmento} - {self.Modalidade}"

     

     