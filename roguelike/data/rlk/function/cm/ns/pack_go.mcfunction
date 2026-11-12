# 무리 공격 시작: 같은 무리(c2G)이고 몸에서 7칸 안, 쉬고 있고 경직 · 빙결이 아닌 졸개 모두
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c2cidS tmp = #cid tmp
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_ns,distance=..7] if score @s c2G = #g tmp if score @s cmS matches 0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s run function rlk:cm/ns/start
scoreboard players operation #cid tmp = #c2cidS tmp
