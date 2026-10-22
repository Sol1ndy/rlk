# @s = body at the centre, field: no travel, slow tracking (3 deg/t), decide when the cooldown is over.
function rlk:mboss/mv/turn {max:3}
execute if score #fgCool mb matches 1.. run scoreboard players remove #fgCool mb 1
execute if score #fgCool mb matches ..0 run function rlk:mboss/fieldgen/ai/next
