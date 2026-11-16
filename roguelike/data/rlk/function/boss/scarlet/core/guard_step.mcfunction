# @s = the guard's probe (at / rotated as it): 0.2 b on toward the step's end while the point keeps 1.6 b from the
# avatar on the floor plane (at most 44 steps: 8.8 b).
execute if score #bx_k hr matches 44.. run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_hr_bxn,distance=..0.2] run return 0
execute positioned ^ ^ ^0.2 positioned ~ 201 ~ if entity @e[tag=rlk_body,distance=..1.6] run return 0
tp @s ^ ^ ^0.2
scoreboard players add #bx_k hr 1
execute at @s run function rlk:boss/scarlet/core/guard_step
