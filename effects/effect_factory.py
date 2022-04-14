from typing import Tuple
from effects import rainbowLine, snake, stars, rainbowBursts, effect, police, solid, two_color

def create_all_list(pixels) -> list[effect.Effect]:
    return [            
        rainbowLine.RainbowLine(pixels, 255),
        snake.Snake(pixels, 30, 8, 255, 0, 0, 0),
        rainbowBursts.RainbowBursts(pixels, 255, 20),
        stars.Stars(pixels, 255, 0, 0 ,0),
        police.Police(pixels, 255),
        two_color.TwoColor(pixels, 255, 255, 0, 0, 0, 255),
        solid.Solid(pixels, 255, 0, 127, 127)
    ]

def create_effect(pixels, effect_definition) -> Tuple[effect.Effect, int, int]:
    new_effect = None
    effect, all_parameters = effect_definition.split(":", 1)
    led_count, frame_delay, *parameters = [int(x) for x in all_parameters.split(";")]

    match effect:
        case "stars":
            new_star_probability, fade_steps, r, g, b, w = parameters
            new_effect = stars.Stars(pixels, r, g, b, w, new_star_probability, fade_steps)
        case "snake":
            snake_length, dimmed_led_count, r, g, b, w = parameters
            new_effect = snake.Snake(pixels, snake_length, dimmed_led_count, r, g, b, w)

    return new_effect, led_count, frame_delay