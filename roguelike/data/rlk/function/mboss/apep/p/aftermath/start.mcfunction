# STUB (AP-CORE, ap_contract 1.3): 종말의 여파 (aftermath, id 32); the pattern stage AP-P3 replaces this file.
# #apq32 = the aftermath clock (-1 while the approach runs).
scoreboard players set #apq32 mb -1
function rlk:mboss/apep/play/crouch_p3
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..2,limit=1] run function rlk:mboss/apep/p/aftermath/go
