# STUB (AP-CORE, ap_contract 1.3): 발광하는 파수꾼 (glow, id 3); the pattern stage replaces this file.
# keeps time only (the clip of each step at its clock; no hazards)
execute if score #apPT mb matches 39 run execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run tp @s ~ 201 ~
execute if score #apPT mb matches 44 run function rlk:mboss/apep/play/emerge_crown_p1
execute if score #apPT mb matches 84..93 run function rlk:mboss/mv/turn {max:6}
execute if score #apPT mb matches 94 run function rlk:mboss/apep/play/glow_slams
execute if score #apPT mb matches 200 run function rlk:mboss/apep/p/release
execute if score #apPT mb matches 225.. run function rlk:mboss/apep/p/end
