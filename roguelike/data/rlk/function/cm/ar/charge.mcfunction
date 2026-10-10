scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
# 마지막 6틱은 조준 고정(궤적이 굵어짐) — 피할 시간
execute if score @s cmT > #cmW_arL tmp positioned ~ ~1.45 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #cid tmp run function rlk:cm/ar/line
execute if score @s cmT = #cmW_arL tmp as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #cid tmp run function rlk:cm/ar/lock
execute if score @s cmT matches ..0 run function rlk:cm/ar/fire
