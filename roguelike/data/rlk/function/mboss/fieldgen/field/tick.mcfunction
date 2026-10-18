# @s = body, every module tick while #fgField >= 1: the field-pattern clock, the first field's hint, the floating
# pebbles around the player while low gravity holds.
execute if score #fgField mb matches 3 run scoreboard players add #fgFT mb 1
execute if score #fgOpen mb matches 1 if score #fgHintT mb matches ..120 run scoreboard players add #fgHintT mb 1
execute if score #fgHintT mb matches 120 if score #fgFN mb matches 1 run function rlk:mboss/fieldgen/hud/refresh
scoreboard players operation #fgM mb = #fgClk mb
scoreboard players operation #fgM mb %= #fgK10 mb
execute if score #fgLowG mb matches 1 if score #fgM mb matches 0 at @e[tag=rlk_body,limit=1] run function rlk:mboss/fieldgen/cfx/pebbles
