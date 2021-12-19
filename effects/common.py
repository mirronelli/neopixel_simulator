def color_function(i, steps, max):
    sixth = steps/6
    i = i % steps

    # full function: /¯¯\__
    # /
    if (i < sixth):
        return int((i*max) / sixth)
    # /¯¯
    if (i < 3 * sixth):
        return int(max)
    # /¯¯\
    if (i < 4 * sixth):
        return int(max * (1 - (i - 3*sixth) / sixth)) 
    # /¯¯\__
    return 0

def create_gamma_table(gamma):
    return [round(pow(i / 255, gamma) * 255) for i in range(256)]