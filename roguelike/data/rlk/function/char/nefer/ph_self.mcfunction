# 환영극 · 네페르 (@s = 플레이어, at 몸): 앞쪽 3칸 풀 원소 범위 피해(일반 공격). 기만의 장막 스택당 +8%
$function rlk:char/nefer/calc {a:$(a),e:$(e)}
function rlk:char/nefer/veil_bonus {p:8}
scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #basic itv 1
execute rotated ~ 0 positioned ^ ^ ^1.5 run tag @e[tag=rlk_mob,distance=..3] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute if score #hitLanded tmp matches 1 run function rlk:combat/on_hit
scoreboard players set #basic itv 0
function rlk:char/after_hit
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
$scoreboard players set #fxId tmp $(fx)
function rlk:char/fx/play
