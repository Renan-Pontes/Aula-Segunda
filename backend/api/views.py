from django.shortcuts import render

from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import CalculosDeJuros
from .serializers import CalculosDeJurosSerializer, MesSerializer, CNPJSerializer

# Create your views here, post/get
@extend_schema(methods=['GET'], responses=CalculosDeJurosSerializer(many=True))
@extend_schema(methods=['POST'], request=CalculosDeJurosSerializer, responses={201: CalculosDeJurosSerializer})
@api_view(['GET', 'POST'])
def CalculosDeJurosListCreateView(request):
    #get logic
     if request.method == 'GET':
          calculos_de_juros = CalculosDeJuros.objects.all()
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)

     if request.method == 'POST':
          data = json.loads(request.body)
          calculo = CalculosDeJuros.objects.create(
               InicioPeriodo=data['InicioPeriodo'],
               FimPeriodo=data['FimPeriodo'],
               CodigoSegmento=data['CodigoSegmento'],
               Segmento=data['Segmento'],
               CodigoModalidade=data['CodigoModalidade'],
               Modalidade=data['Modalidade'],
               Posicao=data['Posicao'],
               InstituicaoFinanceira=data['InstituicaoFinanceira'],
               CNPJ8=data['CNPJ8'],
               TaxaJurosAoMes=data['TaxaJurosAoMes'],
               TaxaJurosAoAno=data['TaxaJurosAoAno'],
          )
          return JsonResponse({
               'InicioPeriodo': calculo.InicioPeriodo,
               'FimPeriodo': calculo.FimPeriodo,
               'CodigoSegmento': calculo.CodigoSegmento,
               'Segmento': calculo.Segmento,
               'CodigoModalidade': calculo.CodigoModalidade,
               'Modalidade': calculo.Modalidade,
               'Posicao': calculo.Posicao,
               'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
               'CNPJ8': calculo.CNPJ8,
               'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
               'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
          }, status=201)


@extend_schema(
     methods=['GET'],
     parameters=[OpenApiParameter('mes', int, description='Mês (1-12) do InicioPeriodo')],
     responses=CalculosDeJurosSerializer(many=True),
)
@extend_schema(methods=['POST'], request=MesSerializer, responses=CalculosDeJurosSerializer(many=True))
@api_view(['GET', 'POST'])
def GetJurosMesView(request):
     if request.method == 'GET':
          mes = request.GET.get('mes')
          calculos_de_juros = CalculosDeJuros.objects.filter(InicioPeriodo__month=mes)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)
     if request.method == 'POST':
          data = json.loads(request.body)
          mes = data.get('mes')
          calculos_de_juros = CalculosDeJuros.objects.filter(InicioPeriodo__month=mes)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)

@extend_schema(
     methods=['GET'],
     parameters=[OpenApiParameter('cnpj', str, description='CNPJ8 da instituição financeira')],
     responses=CalculosDeJurosSerializer(many=True),
)

@extend_schema(methods=['POST'], request=CNPJSerializer, responses=CalculosDeJurosSerializer(many=True))
@api_view(['GET', 'POST'])
def BuscarCNPJView(request):
     if request.method == 'GET':
          cnpj = request.GET.get('cnpj')
          calculos_de_juros = CalculosDeJuros.objects.filter(CNPJ8=cnpj)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)
     if request.method == 'POST':
          data = json.loads(request.body)
          cnpj = data.get('cnpj')
          calculos_de_juros = CalculosDeJuros.objects.filter(CNPJ8=cnpj)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)

@extend_schema(
     methods=['GET'],
     parameters=[OpenApiParameter('nome', str, description='Nome da instituição financeira')],
     responses=CalculosDeJurosSerializer(many=True),
)
@extend_schema(methods=['POST'], request=CNPJSerializer, responses=CalculosDeJurosSerializer(many=True))
@api_view(['GET', 'POST'])
def ScorePorNomeView(request):
     if request.method == 'GET':
          nome = request.GET.get('nome')
          calculos_de_juros = CalculosDeJuros.objects.filter(InstituicaoFinanceira__icontains=nome)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)
     if request.method == 'POST':
          data = json.loads(request.body)
          nome = data.get('nome')
          calculos_de_juros = CalculosDeJuros.objects.filter(InstituicaoFinanceira__icontains=nome)
          data = []
          for calculo in calculos_de_juros:
               data.append({
                    'InicioPeriodo': calculo.InicioPeriodo,
                    'FimPeriodo': calculo.FimPeriodo,
                    'CodigoSegmento': calculo.CodigoSegmento,
                    'Segmento': calculo.Segmento,
                    'CodigoModalidade': calculo.CodigoModalidade,
                    'Modalidade': calculo.Modalidade,
                    'Posicao': calculo.Posicao,
                    'InstituicaoFinanceira': calculo.InstituicaoFinanceira,
                    'CNPJ8': calculo.CNPJ8,
                    'TaxaJurosAoMes': str(calculo.TaxaJurosAoMes),
                    'TaxaJurosAoAno': str(calculo.TaxaJurosAoAno),
               })
          return JsonResponse(data, safe=False)