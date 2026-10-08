# 검기 한 줄기 (@s = 플레이어, 위치·방향 = 시전 자리). macro: c = 피해 계수(%), e = 잠식(%, 0 = 기본). 앞쪽 9칸 부채꼴의 적에게 공허 원소 피해(원소폭발 피해)
$function rlk:char/dmg_calc {coef:$(c)}
function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 8
scoreboard players set #elU tmp 1000
$scoreboard players set #rnErAdd tmp $(e)
tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
execute positioned ^ ^ ^3 run tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute positioned ^ ^ ^6 run tag @e[tag=rlk_mob,distance=..3.5] add rlk_hit
execute positioned ^ ^ ^9 run tag @e[tag=rlk_mob,distance=..3.5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/after_hit
function rlk:char/ronova/wave_fx
