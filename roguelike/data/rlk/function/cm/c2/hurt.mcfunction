# 무리 몹이 맞음 (@s = 두뇌, at @s, combat/apply 의 cm/flash 에서): 0.25초 경직 · 멀리 밀림 · 붉게 번쩍
scoreboard players set @s cmAH 5
execute if score @s stunT matches 1.. run scoreboard players operation @s stunT = #c2Stun tmp
execute if score #stunHit tmp matches 1 run function rlk:cm/c2/knock
execute unless score #stunHit tmp matches 1 if score #basic itv matches 1 run function rlk:cm/c2/knock
scoreboard players operation #fid tmp = @s cmId
execute as @e[tag=rlk_c2pt,distance=..6] if score @s cmId = #fid tmp run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
execute if entity @s[tag=rlk_cm_dr] run function rlk:cm/dr/interrupt
execute if entity @s[tag=rlk_c2slime] run execute unless score #c2shurt snd matches 1 run function rlk:cm/c2/snd/shurt
