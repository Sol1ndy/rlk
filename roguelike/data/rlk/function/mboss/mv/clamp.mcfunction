# @s (e.g. a destination marker) is pulled toward the arena axis until it is inside the fight arena's safe disc.
# A chapter arena (#mbAr >= 1) through F:mboss/ar/<aid>/clamp; the plaza's lines (= ar/plaza/clamp) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/clamp
scoreboard players set #cl mb 0
function rlk:mboss/ar/plaza/clamp_step
