from math import dist
import numpy


def Hipotenuza(vector1, vector2) -> int:
    v1 = numpy.array(vector1)
    v2 = numpy.array(vector2)
    
    hipotenuza = dist(v1,v2)

    return hipotenuza

def Angulo(vector1, vector2) -> int:
    v1 = numpy.array(vector1)
    v2 = numpy.array(vector2)
    angulo = numpy.degrees(numpy.arctan2(*(v2-v1)))
    return angulo if angulo > 0 else 180 + (180+angulo)
