# 중력의 물결 한 번 (@s = 플레이어, 위치 = 몸): 반경 4칸 물 원소 범위 피해(최대 체력 #cgRipPm ‰)
scoreboard players operation #t1 itv = #cgRipPm tmp
execute store result storage rlk:cg pm int 1 run scoreboard players get #t1 itv
function rlk:items/proc/cg_rip_calc with storage rlk:cg
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
function rlk:char/after_hit
particle minecraft:splash ~ ~0.3 ~ 2.5 0.1 2.5 0 40
particle minecraft:bubble_pop ~ ~0.5 ~ 2.5 0.3 2.5 0.02 20
playsound minecraft:entity.player.splash master @a ~ ~ ~ 0.4 1.5
