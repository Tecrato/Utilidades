import tinify, os, dotenv
# pip install python-dotenv
#ejemplo

# clase = Utilidades.recursos.tinify_API.Compress_img()

dotenv.load_dotenv()

img = 'C:/Users/Edouard/Documents/Universidad/Proyecto/Diagramas/MODELADO DE NEGOCIO/DCDU FACTURACION2.png'
img = "C:/Users/Edouard/Pictures/logo-nobg.png"
# clase.compress_file(img,'C:/Users/Edouard/Pictures/Naruto.jpg')

class Compress_img:
    def compress_file(self, img, destino):
        tinify.key = os.environ["API_KEY"]
        source = tinify.from_file(img)
        source.to_file(destino)

# Compress_img().compress_file(img,'C:/Users/Edouard/Pictures/logo-nobg.png')
