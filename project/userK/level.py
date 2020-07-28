def op(op):

    def r(op, max, deltamax, dif):
        for i in range(0, 981):
            if op < max:
                return {'rating': str(op) + '/' + str(max), 'lvl': i, 'dif': dif}
            else:
                max += deltamax

    if op < 1000:
        max = 100
        deltamax = 100
        dif = 'J'
        return r(op, max, deltamax, dif)
    elif op < 3000:
        max = 1000
        deltamax = 200
        dif = 'L'
        return r(op, max, deltamax, dif)
    elif op < 6000:
        max = 3000
        deltamax = 300
        dif = 'Z'
        return r(op, max, deltamax, dif)
    elif op < 10000:
        max = 6000
        deltamax = 400
        dif = 'M'
        return r(op, max, deltamax, dif)
    else:
        max = 10000
        deltamax = 500
        dif = 'P'
        return r(op, max, deltamax, dif)