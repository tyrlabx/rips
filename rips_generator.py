import pandas as pd
import json
import streamlit as st

#{'numDocumentoldObligado': '814006170', 'numFactura': 'CTFE226713', 'tipoNota': None, 'numNota': None, 'usuarios': [{'tipoDocumentoldentificacion': 'CC', 'numDocumentoldentificacion': '52100200', 'tipoUsuario': '01', 'fechaNacimiento': '2000-01-01', 'codSexo': 'M', 'codPaisResidencia': '170', 'codMunicipioResidencia': '05134', 'codZonaTerritorialResidencia': '01', 'incapacidad': '02', 'consecutivo': 1, 'codPaisOrigen': '170', 'servicios': {'consultas': [{'codPrestador': '500000000001', 'fechalnicioAtencion': '2021-08-18 08:10', 'numAutorizacion': '100000000002', 'codConsulta': '890201', 'modalidadGrupoServicioTecSal': '09', 'grupoServicios': '01', 'codServicio': 1, 'finalidadTecnologiaSalud': '11', 'causaMotivoAtencion': '21', 'codDiagnosticoPrincipal': 'D482', 'codDiagnosticoRelacionado1': 13428, 'codDiagnosticoRelacionado2': None, 'codDiagnosticoRelacionado3': None, 'tipoDiagnosticoPrincipal': '01', 'tipoDocumentoldentificacion': 'CC', 'numDocumentoldentificacion': '80100200', 'vrServicio': 36341, 'tipoPagoModerador': '01', 'valorPagoModerador': 8000, 'numFEVPagoModerador': 'AF0987232XX', 'consecutivo': 1}]}}]}
st.subheader(":one: Por favor, descargar la plantilla")
with open('plantilla_RIPS.xlsx', 'rb') as f:
   st.download_button('Descargar plantilla', f, file_name='plantilla_RIPS.xlsx')  # Defaults to 'application/octet-stream'
st.subheader(":two: Por favor, cargar la plantilla con los datos diligenciados")
uploaded_file = st.file_uploader("Cargar la plantilla excel")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    try: 
        temp = pd.read_excel(bytes_data, sheet_name=None)
    except Exception as e:
        st.exception(f'El archivo cargado no es valido, contacta al administrador.{e}')
    usuarios = [temp.get('usuarios').to_dict()]
    consultas = temp.get('consultas')
    procedimientos = temp.get('procedimientos')
    otrosServicios = temp.get('otros')

    rips = temp.get('facturas').to_dict()
    rips['usuarios'] = []
    tecnologies = dict()
    for user in usuarios:
        ssn = user.get('numDocumentoldentificacion')
        consultas = consultas[consultas['numDocumentoldentificacion'] == ssn]
        procedimientos = procedimientos[procedimientos['numDocumentoldentificacion'] == ssn]
        otrosServicios = otrosServicios[otrosServicios['numDocumentoldentificacion'] == ssn]
        tecnologies['serviciosTecnologias'] = []
        tecnologies['serviciosTecnologias'].append({'consultas': [consultas.to_dict()], 'procedimientos': [procedimientos.to_dict()],
         'otrosServicios':[otrosServicios.to_dict()]})
        rips['usuarios'].append(tecnologies)
    try:
        result = json.dumps(rips)
        st.success('Se ha cargado el archivo correctamente, por favor da click en Generar RIPS para descargar.')
    except Exception as e:
        st.exception('No ha sido posible procesar la información, contacta al administrador.')
        result = ''
    if st.download_button('Generar RIPS',result, file_name='nuevos_rips.json'):
        st.balloons()
        st.success('El archivo ha sido descargado, por favor revisa tu directorio de descargas.')
