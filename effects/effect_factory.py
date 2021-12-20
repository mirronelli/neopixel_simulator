from effects import rainbowLine, snake, stars, rainbowBursts, effect, police, solid

def create_all_list(pixels) -> list[effect.Effect]:
    return [            
        rainbowLine.RainbowLine(pixels, 255),
        snake.Snake(pixels, 30, 8, 255, 0, 0, 0),
        rainbowBursts.RainbowBursts(pixels, 255, 20),
        stars.Stars(pixels, 255, 0, 0 ,0),
        police.Police(pixels, 255),
        solid.Solid(pixels, 255, 0, 127, 127)
    ]