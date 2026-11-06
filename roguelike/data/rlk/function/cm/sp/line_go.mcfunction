# 대열 공격 시작: 같은 대열(c2G)로 8칸 안, 쉬고 있고 경직 · 빙결이 아닌 창병 모두 (각자 지금 바라보는 쪽으로)
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c2cidS tmp = #cid tmp
execute as @e[tag=rlk_cm_sp,distance=..8] if score @s c2G = #g tmp if score @s cmS matches 0 if score @s cmAR matches ..0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s run function rlk:cm/sp/start
scoreboard players operation #cid tmp = #c2cidS tmp
