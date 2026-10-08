# 선택 해제: 라벨 원래 크기 (@s = 버튼, at @s)
tag @s remove rlk_dhov_on
data modify entity @e[tag=rlk_dlbl,distance=..0.5,limit=1,sort=nearest] transformation.scale set value [0.82f,0.82f,0.82f]
