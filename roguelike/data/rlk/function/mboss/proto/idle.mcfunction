execute if score #prCool mb matches 1.. run scoreboard players remove #prCool mb 1
function rlk:mboss/mv/turn {max:12}
execute unless entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/mv/toward {d:0.16}
execute if score #prCool mb matches ..0 run function rlk:mboss/proto/choose
