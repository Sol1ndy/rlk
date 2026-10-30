# 치유 한 번 (2초마다): 8칸 안의 다친 커스텀 몹 두뇌(나 말고) 모두 +최대 체력 10 %, 최대 체력에서 멈춤. 물줄기를 그림
scoreboard players operation @s c3H = #c3Hi_cw tmp
tag @s add rlk_c3heal
execute as @e[tag=rlk_cmb,distance=..8] unless score @s cmId = #cid tmp if score @s mhpC < @s mhpM at @s run function rlk:cm/cw/heal_one
tag @s remove rlk_c3heal
particle minecraft:splash ~ ~2.4 ~ 0.3 0.3 0.3 0.2 20 normal
execute unless score #c3cwheal snd matches 1 run function rlk:cm/c3/snd/cwheal
execute unless score #c3cwchime snd matches 1 run function rlk:cm/c3/snd/cwchime
