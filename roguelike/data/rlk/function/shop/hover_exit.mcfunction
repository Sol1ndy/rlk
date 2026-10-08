# 선택 해제: 라벨 원래 크기 (@s = 버튼, at @s)
tag @s remove rlk_shop_hov_on
data modify entity @e[tag=rlk_shop_lbl,distance=..0.6,limit=1,sort=nearest] transformation.scale set value [0.85f,0.85f,0.85f]
data modify entity @e[tag=rlk_shop_rlbl,distance=..0.6,limit=1,sort=nearest] transformation.scale set value [0.85f,0.85f,0.85f]
