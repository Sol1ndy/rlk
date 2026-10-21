# STUB (AP-CORE, ap_contract 1.3): 생명의 꼬리 (tail3, id 34); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apq34 mb matches 1 if score #apPT mb matches 8 run function rlk:boss/apep/play/walk_p3
execute if score #apq34 mb matches 1 if score #apPT mb matches 9..37 at @e[tag=rlk_body,limit=1] unless entity @s[distance=..4] as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.2 run function rlk:boss/apep/u/step_here
execute if score #apq34 mb matches 1 if score #apPT mb matches 9..37 run function rlk:mboss/mv/turn {max:6}
execute if score #apq34 mb matches 0 if score #apPT mb matches 8 run function rlk:boss/apep/play/tail_p3
execute if score #apq34 mb matches 1 if score #apPT mb matches 38 run function rlk:boss/apep/play/tail_p3
execute if score #apq34 mb matches 0 if score #apPT mb matches 62 run function rlk:boss/apep/p/release
execute if score #apq34 mb matches 1 if score #apPT mb matches 92 run function rlk:boss/apep/p/release
execute if score #apPT mb >= #apPLen mb run function rlk:boss/apep/p/end
