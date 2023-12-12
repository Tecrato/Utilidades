import tinify

#ejemplo

# clase = Utilidades.recursos.tinify_API.Compress_img()

# img = 'C:/Users/Edouard/Pictures/1626311193_Naruto - boruto (383).jpg'

# clase.compress_file(img,'C:/Users/Edouard/Pictures/Naruto.jpg')

class Compress_img:
    def compress_file(self, img, destino):
        tinify.key = '3V8Kkx6pmrWy4g6cZtNVcBYWnjhQj8HK'
        source = tinify.from_file(img)
        source.to_file(destino)

    