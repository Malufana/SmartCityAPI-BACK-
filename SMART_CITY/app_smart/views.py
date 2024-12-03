from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from app_smart.models import Sensor, LuminosidadeData, TemperaturaData, UmidadeData, ContadorData
from django.views.generic import TemplateView
import logging
from .forms import CSVUploadForm
import csv
from dateutil import parser
import pytz
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
import uuid
# import authenticate
# from API.serializers import CreateSensorSerializer
# from rest_framework.response import Response
# from rest_framework import status

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# @api_view(['GET', 'POST'])
# def criarSensor(request):
#     if request.method == 'GET':
#         queryset = Sensor.objects.all()
#         serializer = CreateSensorSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CreateSensorSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
def abre_index(request):
    mensagem = "OLÁ TURMA, SEJAM FELIZES SEMPRE!"
    return HttpResponse(mensagem)

class CSVUploadView(TemplateView):
    template_name = 'upload.html'

class CSVUploadForm(forms.Form):
    sensor_csv = forms.FileField(required=False)
    luminosidade_csv = forms.FileField(required=False)
    temperatura_csv = forms.FileField(required=False)
    umidade_csv = forms.FileField(required=False)
    contador_csv = forms.FileField(required=False)

def process_csv_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        upload_type = request.POST.get('upload_type')
        
        print(request.POST)
        print(request.FILES)
        print(f"Tipo de upload recebido: {upload_type}")


        if form.is_valid():
            if upload_type == 'sensor':
                csv_file = request.FILES.get('sensor_csv')
            elif upload_type == 'luminosidade':
                csv_file = request.FILES.get('luminosidade_csv')
            elif upload_type == 'temperatura':
                csv_file = request.FILES.get('temperatura_csv')
            elif upload_type == 'umidade':
                csv_file = request.FILES.get('umidade_csv')
            elif upload_type == 'contador':
                csv_file = request.FILES.get('contador_csv')
            else:
                form.add_error(None, 'Tipo de upload inválido.')
                return render(request, 'app_smart/upload.html', {'form': form})
        
            # Verifica se o arquivo tem a extensão correta
            if not csv_file.name.endswith('.csv'):
                form.add_error(csv_file.name, 'Este não é um arquivo CSV válido.')
            else:
                
                # Processa o arquivo CSV
                file_data = csv_file.read().decode('ISO-8859-1').splitlines()
                print(file_data)
                reader = csv.DictReader(file_data, delimiter=',')  # Altere para ',' se necessário
                
                
                #Processamento baseado no tipo de upload
                if upload_type == 'sensor': #Processamento de arquivos tipo sensor
                    csv_file = request.FILES.get('sensor_csv')
                    for row in reader:
                        try:
                            Sensor.objects.create(
                                tipo=row['tipo'],
                                unidade_medida=row['unidade_medida'] if row['unidade_medida'] else None,
                                latitude=float(row['latitude'].replace(',', '.')),
                                longitude=float(row['longitude'].replace(',', '.')),
                                localizacao=row['localizacao'],
                                responsavel=row['responsavel'] if row['responsavel'] else '',
                                status_operacional=True if row['status_operacional'] == 'True' else False,
                                observacao=row['observacao'] if row['observacao'] else '',
                                mac_address=row['mac_address'] if row['mac_address'] else None
                            )
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")  # Exibe o erro e a linha problemática

                elif upload_type == 'luminosidade': #Processamento do tipo luminosidade
                    csv_file = request.FILES.get('luminosidade_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            LuminosidadeData.objects.create(sensor=sensor, valor=valor,
                            timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

                elif upload_type == 'temperatura':
                    csv_file = request.FILES.get('temperatura_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            TemperaturaData.objects.create(sensor=sensor, valor=valor, timestamp=timestamp)
                            line_count += 1
                            if line_count% 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")
                        
                elif upload_type == 'umidade':
                    csv_file = request.FILES.get('umidade_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp']).astimezone(pytz.timezone('America/Sao_Paulo'))
                            sensor = Sensor.objects.get(id=sensor_id)
                            UmidadeData.objects.create(sensor=sensor, valor=valor, timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

                elif upload_type == 'contador':
                    csv_file = request.FILES.get('contador_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            ContadorData.objects.create(sensor=sensor, timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

        else:
            print(form.errors)   

    else:
        form = CSVUploadForm()

    return render(request, 'app_smart/upload.html', {'form': form})

@api_view(['POST'])
def process_upload(request):

    if request.method == 'POST':
        upload_type = request.POST.get('upload_type')
        unique_id = str(uuid.uuid4())
        print(f"Upload type recebido: '{upload_type}'")
        print(f"Todos os dados recebidos: {request.POST}")
        print(f"Arquivos recebidos: {request.FILES}")

        if upload_type == 'sensor':
            file = request.FILES.get('sensor_csv')
            model = Sensor
        elif upload_type == 'luminosidade':
            file = request.FILES.get('luminosidade_csv')
            model = LuminosidadeData
        elif upload_type == 'temperatura':
            file = request.FILES.get('temperatura_csv')
            model = TemperaturaData
        elif upload_type == 'umidade':
            file = request.FILES.get('umidade_csv')
            model = UmidadeData
        elif upload_type == 'contador':
            file = request.FILES.get('contador_csv')
            model = ContadorData
        else:
            return JsonResponse({'status': 'failed', 'message': 'Tipo de upload desconhecido'})

        if file:
            file_name = f"{unique_id}_{file.name}"
            default_storage.save(file_name, file)
            # return JsonResponse({'status': 'success', 'file_name': file_name})
            try:
                with default_storage.open(file_name, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)

                    for row in reader:
                        if upload_type == 'sensor':
                            model.objects.create(
                                tipo = row[0],
                                mac_address = row[1],
                                latitude = row[2],
                                longitude = row[3],
                                localizacao = row[4],
                                responsavel = row[5],
                                unidade_medida = row[6],
                                status_operacional = row[7],
                                observacao = row[8]
                            )

                        elif upload_type == 'luminosidade':
                            model.objects.create(
                                valor = row[0],
                                sensor_id = row[1],
                                timestamp = row[2]
                            )

                        elif upload_type == 'temperatura':
                            model.objects.create(
                                valor = row[0],
                                sensor_id = row[1],
                                timestamp = row[2]
                            )

                        elif upload_type == 'umidade':
                            model.objects.create(
                                sensor_id = row[0],
                                valor = row[1],
                                timestamp = row[2]
                            )

                        elif upload_type == 'contador':
                            model.objects.create(
                                sensor_id = row[0],
                                timestamp = row[1]
                            )

                    return JsonResponse({'status': 'success', 'file_name': file_name})

            except Exception as e:
                print(f"Erro ao processar o CSV: {e}")
                return JsonResponse({'status': 'failed', 'message': f'Erro ao processar o CSV: {e}'})
            
        else:
            return JsonResponse({'status': 'failed', 'message': 'Nenhum arquivo enviado'})
        
    return JsonResponse({'status': 'failed', 'message': 'Método não permitido'}, status=405)


# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     usuario = authenticate('username', 'password')

#     if usuario is not None:
#         return JsonResponse({'status': 'success', 'message': 'Usuario Logado com sucesso'})
#     else:
#         return JsonResponse({'status': 'failed', 'message': 'Falha ao logar usuario'})

    