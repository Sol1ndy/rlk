# The cs1 skip input (@s = the body, every tick of the sequence; v_brief VC 5): from 40 to 560 the prompt
# ⊙ 건너뛰기 · Space 길게; holding the jump key (rlk:in_jump) brightens it in 4 steps of 5 t, a release
# resets the count; 20 t held -> the skip (skipgo: seq/cs1/skip, then #sq = 565: the next tick is 566).
# The core's Shift input (core/skip) rests while #skip is -1.
scoreboard players set #skip hr -1
execute if score #sq_skd hr matches 1 run return 0
execute if score #skp hr matches 1.. if score #sq hr = #skp hr run return run function rlk:boss/scarlet/seq/cs1/skipgo
execute if score #sq hr matches 561.. run return run function rlk:boss/scarlet/seq/cs1/skipoff
execute unless score #sq hr matches 40..560 run return 0
execute as @a[tag=player,limit=1] if predicate rlk:in_jump run scoreboard players add #sq_sk hr 1
execute as @a[tag=player,limit=1] unless predicate rlk:in_jump run scoreboard players set #sq_sk hr 0
execute if score #sq_sk hr matches 20.. run return run function rlk:boss/scarlet/seq/cs1/skipgo
execute if score #sq_sk hr matches 0 unless score #sq_sks hr matches 0 as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:{text:"",extra:[{text:"⊙ 건너뛰기",color:"#A8A8B0"},{text:" · Space 길게",color:"#A8A8B0"}]},background:-1207959552}
execute if score #sq_sk hr matches 0 unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar {text:"",extra:[{text:"⊙ 건너뛰기",color:"#A8A8B0"},{text:" · Space 길게",color:"#A8A8B0"}]}
execute if score #sq_sk hr matches 0 run scoreboard players set #sq_sks hr 0
execute if score #sq_sk hr matches 1..5 unless score #sq_sks hr matches 1 as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:{text:"",extra:[{text:"⊙ 건너뛰기",color:"#BEBEC5"},{text:" · Space 길게",color:"#A8A8B0"}]},background:-1207959552}
execute if score #sq_sk hr matches 1..5 unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar {text:"",extra:[{text:"⊙ 건너뛰기",color:"#BEBEC5"},{text:" · Space 길게",color:"#A8A8B0"}]}
execute if score #sq_sk hr matches 1..5 run scoreboard players set #sq_sks hr 1
execute if score #sq_sk hr matches 6..10 unless score #sq_sks hr matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:{text:"",extra:[{text:"⊙ 건너뛰기",color:"#D3D3D9"},{text:" · Space 길게",color:"#A8A8B0"}]},background:-1207959552}
execute if score #sq_sk hr matches 6..10 unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar {text:"",extra:[{text:"⊙ 건너뛰기",color:"#D3D3D9"},{text:" · Space 길게",color:"#A8A8B0"}]}
execute if score #sq_sk hr matches 6..10 run scoreboard players set #sq_sks hr 2
execute if score #sq_sk hr matches 11..15 unless score #sq_sks hr matches 3 as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:{text:"",extra:[{text:"⊙ 건너뛰기",color:"#E9E9EC"},{text:" · Space 길게",color:"#A8A8B0"}]},background:-1207959552}
execute if score #sq_sk hr matches 11..15 unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar {text:"",extra:[{text:"⊙ 건너뛰기",color:"#E9E9EC"},{text:" · Space 길게",color:"#A8A8B0"}]}
execute if score #sq_sk hr matches 11..15 run scoreboard players set #sq_sks hr 3
execute if score #sq_sk hr matches 16..19 unless score #sq_sks hr matches 4 as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:{text:"",extra:[{text:"⊙ 건너뛰기",color:"#FFFFFF"},{text:" · Space 길게",color:"#A8A8B0"}]},background:-1207959552}
execute if score #sq_sk hr matches 16..19 unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar {text:"",extra:[{text:"⊙ 건너뛰기",color:"#FFFFFF"},{text:" · Space 길게",color:"#A8A8B0"}]}
execute if score #sq_sk hr matches 16..19 run scoreboard players set #sq_sks hr 4
scoreboard players set @a[tag=player] hudHold 2
