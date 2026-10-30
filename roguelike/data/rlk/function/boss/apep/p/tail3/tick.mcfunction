# 생명의 꼬리 (tail3, id 34; plan 8.3). tick (#apq34T = the tail_p3 tick; negative during the crouch / walk opener).
scoreboard players operation #apq34T mb = #apPT mb
scoreboard players operation #apq34T mb -= #apq34O mb
execute if score #apq34T mb matches ..-1 run function rlk:mboss/mv/turn {max:6}
execute if score #apq34 mb matches 1 if score #apPT mb matches 8 run function rlk:boss/apep/play/walk_p3
execute if score #apq34 mb matches 1 if score #apq34T mb matches ..-1 if score #apPT mb matches 9.. at @e[tag=rlk_body,limit=1] unless entity @s[distance=..5] as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.2 run function rlk:boss/apep/u/step_here
execute if score #apq34T mb matches 87.. run return run function rlk:boss/apep/p/tail3/done
execute if score #apq34T mb matches 0..32 run return run function rlk:boss/apep/p/tail3/kd/0_32
execute if score #apq34T mb matches 36..54 run return run function rlk:boss/apep/p/tail3/kd/36_54
