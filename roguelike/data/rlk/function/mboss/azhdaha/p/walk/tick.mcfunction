execute if score #azWk mb matches 0 if score #azPT mb matches ..39 run function rlk:mboss/mv/turn {max:4}
execute if score #azWk mb matches 0 if score #azPT mb matches ..39 run function rlk:mboss/azhdaha/u/fwd {d:0.13}
execute if score #azWk mb matches 0 if entity @e[tag=rlk_body,distance=..9,limit=1] run function rlk:mboss/azhdaha/p/walk/stop
execute if score #azWk mb matches 0 if score #azPT mb matches 40.. run function rlk:mboss/azhdaha/p/walk/stop
execute if score #azWk mb matches 1.. run scoreboard players add #azWk mb 1
execute if score #azWk mb matches 17.. run function rlk:mboss/azhdaha/p/end
