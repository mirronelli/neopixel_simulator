def color_function(i, steps):
    sixth = steps/6
    i = i % steps

    # full function: /¯¯\__
    # /
    if (i < sixth):
        return (i / sixth)
    # /¯¯
    if (i < 3 * sixth):
        return 1
    # /¯¯\
    if (i < 4 * sixth):
        return 1 - (i - 3*sixth) / sixth
    # /¯¯\__
    return 0