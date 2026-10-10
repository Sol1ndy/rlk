# 다음 틱부터 cmV 틱 동안 가득 차오름
tag @s remove rlk_cmwg_ic
execute store result entity @s interpolation_duration int 1 run scoreboard players get @s cmV
data merge entity @s {start_interpolation:0,transformation:{translation:[-1.610f,0f,-1.610f],scale:[3.220f,0.02f,3.220f]}}
