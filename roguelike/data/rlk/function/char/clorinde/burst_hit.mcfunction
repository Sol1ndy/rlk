# 참격 한 번 (@s = 플레이어, 위치·방향 = 발동한 자리): 3.5칸 앞을 중심으로 반경 4.5칸 + 발동 자리 반경 2칸
function rlk:char/dmg_calc {coef:127}
function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,distance=..2] add rlk_hit
execute positioned ^ ^ ^3.5 run tag @e[tag=rlk_mob,distance=..4.5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute positioned ^ ^1 ^3 run particle minecraft:sweep_attack ~ ~ ~ 1.8 0.8 1.8 0 6
execute positioned ^ ^1 ^3 run particle minecraft:electric_spark ~ ~ ~ 1.8 0.8 1.8 0.4 30
execute positioned ^ ^1 ^3 run particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:1.4f} ~ ~ ~ 2.0 0.9 2.0 0 14
execute unless score #k259 snd matches 1 run function rlk:snd/f290
execute unless score #k257 snd matches 1 run function rlk:snd/f288
execute unless score #k260 snd matches 1 run function rlk:snd/f291
