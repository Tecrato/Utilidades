import requests
from urllib.parse import quote

def check_update(program_name:str,version_actual:str,version_deseada='last'):
    response = requests.get(f'https://tecrato.pythonanywhere.com/api/programs?program={quote(program_name)}&version={quote(version_deseada)}')

    resultado = response.json()
    if resultado['status'] == 'error':
        return False
    version_actual = version_actual.split('.')
    version_internet = resultado['version'].split('.')
    cuenta_versiones = max(len(version_actual),len(version_internet))


    for x in range(cuenta_versiones):
        version_actual.append(0)
        version_internet.append(0)
        if int(version_internet[x]) > int(version_actual[x]):
            return {'version': resultado['version'], 'url': resultado['url']}
    else:
        return False