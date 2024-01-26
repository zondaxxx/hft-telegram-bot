from random import shuffle

slovari = [list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
           list('abcdefghijklmnopqrstuvwxyz'),
           list('123456789')]

def test_name(sl = slovari) -> str:
    name = str()
    for _ in range(5):
        shuffle(sl)
        shuffle(sl[0])
        name += sl[0][0]
    return name