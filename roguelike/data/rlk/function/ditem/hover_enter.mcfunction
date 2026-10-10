# 선택됨: 라벨 확대 + 효과음 (@s = 버튼, at @s)
tag @s add rlk_dhov_on
data modify entity @e[tag=rlk_dlbl,distance=..0.5,limit=1,sort=nearest] transformation.scale set value [1.15f,1.15f,1.15f]
execute unless score #k16 snd matches 1 run function rlk:snd/f217
