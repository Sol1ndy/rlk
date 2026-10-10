# 떨어질 자리 표시 (@s): 남은 시간이 지나면 사라짐(보통은 투사체가 터질 때 cm/wd_kill 로 먼저 지워짐)
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run return run kill @s
execute if entity @s[tag=rlk_cmwg_cn] run function rlk:cm/wd/grow_cn
execute if entity @s[tag=rlk_cmwg_ic] run function rlk:cm/wd/grow_ic
