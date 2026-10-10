# 다음 틱부터 cmV 틱 동안 가득 차오름
tag @s remove rlk_cmwg_cn
execute store result entity @s interpolation_duration int 1 run scoreboard players get @s cmV
data merge entity @s {start_interpolation:0,transformation:{translation:[-1.540f,0f,-1.540f],scale:[3.080f,0.02f,3.080f]}}
