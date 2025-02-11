def import_from_file(file_path):
    file = open(file_path, 'r').readlines()[0]
    lista_puntos = []
    for x in file.split('|'):
        lista_puntos.append([float(a) for a in  x.split(',')])

    return lista_puntos