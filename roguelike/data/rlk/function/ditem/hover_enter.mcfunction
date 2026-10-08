# 선택됨: 라벨 확대 + 효과음 (@s = 버튼, at @s)
tag @s add rlk_dhov_on
data modify entity @e[tag=rlk_dlbl,distance=..0.5,limit=1,sort=nearest] transformation.scale set value [1.15f,1.15f,1.15f]
playsound minecraft:block.note_block.hat master @a ~ ~ ~ 0.7 1.9
