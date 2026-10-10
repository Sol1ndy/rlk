# 진실의 눈동자 한 타 (@s = 플레이어, 위치·방향 = 시전 자리): 앞쪽 4칸을 중심으로 반경 4칸 풀 원소 범위 피해(원소폭발 피해)
$function rlk:char/nefer/calc {a:$(a),e:$(e)}
function rlk:items/hook/burst_dmg
scoreboard players set #t1 tmp 13
scoreboard players operation #t1 tmp *= @s nfQV
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 2000
tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
execute positioned ^ ^ ^4 run tag @e[tag=rlk_mob,distance=..4] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/after_hit
particle minecraft:composter ^ ^0.5 ^4 2.5 0.5 2.5 0 50
particle minecraft:dust{color:[0.55,0.95,0.35],scale:2.0} ^ ^0.6 ^4 2.5 0.3 2.5 0 40
execute unless score #k338 snd matches 1 run function rlk:snd/f399
execute unless score #k290 snd matches 1 run function rlk:snd/f325
