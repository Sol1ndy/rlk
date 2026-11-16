# 둘씩 공격: 나 + 같은 무리에서 쉬는 한 마리(무작위). 무리 전체는 다음 쌍까지 #c3Gap_em 틱 기다림. 몸까지 길이 막혔거나 낭떠러지면 안 감
execute unless function rlk:cm/em/dash_ok run return run scoreboard players set @s cmCd 10
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c3cidS tmp = #cid tmp
tag @s add rlk_c3pick
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_em,tag=!rlk_c3pick,distance=..9] if score @s c2G = #g tmp if score @s cmS matches 0 if score @s cmAR matches ..0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s if function rlk:cm/em/dash_ok run tag @s add rlk_c3cand
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_em,distance=..16] if score @s c2G = #g tmp if score @s cmCd < #c3Gap_em tmp run scoreboard players operation @s cmCd = #c3Gap_em tmp
execute as @e[tag=rlk_c3cand,limit=1,sort=random] at @s run function rlk:cm/em/start
function rlk:cm/em/start
tag @e[tag=rlk_c3cand] remove rlk_c3cand
tag @s remove rlk_c3pick
scoreboard players operation #cid tmp = #c3cidS tmp
