# Hook spawn (@s = arena marker at the centre, facing north). The body starts 10 b above the centre star
# and drops in during the intro; it faces the arriving player (south).
execute positioned ~ ~10 ~ rotated 0 0 run function rlk:mboss/body
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/proto/reload
