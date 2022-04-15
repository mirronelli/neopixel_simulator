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
    led_count = 0
    frame_delay = 0

    try:
        effect, all_parameters = effect_definition.split(":", 1)
        led_count, frame_delay, *parameters = [int(x) for x in all_parameters.split(";")]

        if effect == "stars":
                new_star_probability, fade_steps, r, g, b, w = parameters
                print(f'nsp {new_star_probability}, fs {fade_steps}, r{r} g{g} b{b} {w}')
                new_effect = stars.Stars(pixels, r, g, b, w, new_star_probability, fade_steps)
        elif effect == "snake":
                snake_length, dimmed_led_count, r, g, b, w = parameters
                new_effect = snake.Snake(pixels, snake_length, dimmed_led_count, r, g, b, w)
        elif effect == "police":
                brightness = parameters[0]
                new_effect = two_color.TwoColor(pixels, brightness, 0, 0, 0, 0, brightness)
        elif effect == "ukraine":
                brightness = parameters[0]
                new_effect = two_color.TwoColor(pixels, brightness, brightness, 0, 0, 0, brightness)
        elif effect == "rainbow":
                brightness = parameters[0]
                new_effect = rainbowLine.RainbowLine(pixels, brightness)
        elif effect == "rainbow_line":
                brightness = parameters[0]
                new_effect = rainbowLine.RainbowLine(pixels, brightness)
        elif effect == "rainbow_bursts":
                brightness, steps = parameters
                new_effect = rainbowBursts.RainbowBursts(pixels, brightness, steps)
        elif effect == "solid":
                r, g, b, w = parameters
                new_effect = solid.Solid(pixels, r, g, b, w)
    except:
        print("invalid command, ignoring")

    return new_effect, led_count, frame_delay
