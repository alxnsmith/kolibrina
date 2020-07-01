def op(op):

    def r(op, max, deltamax, league):
        for i in range(0, 981):
            if op < max:
                return {'rating': str(op) + '/' + str(max), 'lvl': i + 1, 'league': league}
            else:
                max += deltamax

    if op < 1000:
        max = 100
        deltamax = 100
        league = 'J (юниор)'
        return r(op, max, deltamax, league)
    elif op < 3000:
        max = 1000
        deltamax = 200
        league = 'L'
        return r(op, max, deltamax, league)
    elif op < 6000:
        max = 3000
        deltamax = 300
        league = 'Z'
        return r(op, max, deltamax, league)
    elif op < 10000:
        max = 6000
        deltamax = 400
        league = 'M'
        return r(op, max, deltamax, league)
    else:
        max = 10000
        deltamax = 500
        league = 'P'
        return r(op, max, deltamax, league)