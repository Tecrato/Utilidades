import tinify, decouple

#ejemplo

# clase = Utilidades.recursos.tinify_API.Compress_img()

# img = 'C:/Users/Edouard/Documents/Universidad/Proyecto/Diagramas/MODELADO DE NEGOCIO/DCDU FACTURACION2.png'

# clase.compress_file(img,'C:/Users/Edouard/Pictures/Naruto.jpg')

class Compress_img:
    def compress_file(self, img, destino):
        tinify.key = decouple.config['API_KEY']
        source = tinify.from_file(img)
        source.to_file(destino)


# Compress_img().compress_file(img,'C:/Users/Edouard/Documents/Universidad/Proyecto/Diagramas/MODELADO DE NEGOCIO/DCDU FACTURACION.png')
