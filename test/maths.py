from Utilidades.maths import rect_colition

def test_rext_colition():
    assert rect_colition((0,50,50,50),(51,50,50,50)) == False
    assert rect_colition((100,105,50,50),(0,50,50,50)) == False
    assert rect_colition((51,50,50,50),(0,50,50,50)) == False
    assert rect_colition((0,0,50,50),(0,150,50,50)) == False
    assert rect_colition((0,0,50,50),(0,100,50,50)) == False
    assert rect_colition((0,0,50,50),(0,75,50,50)) == False

    assert rect_colition((0,50,50,50),(45,50,50,50)) == True
    assert rect_colition((0,50,50,50),(49,50,50,50)) == True
    assert rect_colition((10,50,50,50),(10,50,50,50)) == True
    assert rect_colition((40,50,50,50),(0,10,50,50)) == True

    assert rect_colition((0,0,10,10),(0,0,50,50)) == True

    assert rect_colition((-47, -50, 50, 800),(0,0,100,100)) == True


if __name__=="__main__":
    test_rext_colition()