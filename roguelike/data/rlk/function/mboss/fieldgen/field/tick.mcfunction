# @s = body, every module tick while #fgField >= 1: the field-pattern clock, the first field's hint, the field
# ambience (seq_f/field/tick: the pebbles around the player while low gravity holds, ...).
execute if score #fgField mb matches 3 run scoreboard players add #fgFT mb 1
execute if score #fgOpen mb matches 1 if score #fgHintT mb matches ..120 run scoreboard players add #fgHintT mb 1
execute if score #fgHintT mb matches 120 if score #fgFN mb matches 1 run function rlk:mboss/fieldgen/hud/hint_end
function rlk:mboss/fieldgen/seq_f/field/tick
