# @s = body, cruise: track the player (4 deg/t), keep 6-10 b (glide in at 0.18 b/t, out at 0.15 b/t, only
# inside r 16.5), decide when the cooldown is over.
function rlk:mboss/mv/turn {max:4}
execute if score #fgCool mb matches 1.. run scoreboard players remove #fgCool mb 1
function rlk:mboss/fieldgen/ai/loco
execute if score #fgCool mb matches ..0 run function rlk:mboss/fieldgen/ai/next
