# 선택됨: 라벨 확대 + 효과음 (@s = 버튼, at @s)
tag @s add rlk_shop_hov_on
data modify entity @e[tag=rlk_shop_lbl,distance=..0.6,limit=1,sort=nearest] transformation.scale set value [1.1f,1.1f,1.1f]
data modify entity @e[tag=rlk_shop_rlbl,distance=..0.6,limit=1,sort=nearest] transformation.scale set value [1.1f,1.1f,1.1f]
execute unless score #k16 snd matches 1 run function rlk:snd/f217
