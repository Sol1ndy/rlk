# RINGS pattern tick 47
execute if score #ph hr matches 7 run function rlk:mboss/mv/turn {max:10}
execute if score #ph hr matches 7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_on
execute if score #ph hr matches 7 run function rlk:boss/scarlet/rig/anchor/blade_mid
execute if score #ph hr matches 7 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_off
execute if score #ph hr matches 7 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
