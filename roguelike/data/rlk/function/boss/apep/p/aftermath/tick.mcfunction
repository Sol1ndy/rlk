# STUB (AP-CORE, ap_contract 1.3): 종말의 여파 (aftermath, id 32); the pattern stage AP-P3 replaces this file.
execute if score #apq32 mb matches -1 if score #apPT mb matches 8 run function rlk:boss/apep/play/walk_p3
execute if score #apq32 mb matches -1 if score #apPT mb matches 8.. at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.4 run function rlk:boss/apep/u/step_here
execute if score #apq32 mb matches -1 if score #apPT mb matches 8.. positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..1,limit=1] run return run function rlk:boss/apep/p/aftermath/go
execute if score #apq32 mb matches -1 if score #apPT mb matches 58.. run return run function rlk:boss/apep/p/aftermath/go
execute if score #apq32 mb matches 0.. run scoreboard players add #apq32 mb 1
execute if score #apq32 mb matches 176 run function rlk:boss/apep/p/release
execute if score #apq32 mb matches 224.. run function rlk:boss/apep/p/end
