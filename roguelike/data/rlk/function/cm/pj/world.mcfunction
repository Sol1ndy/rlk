# round V: 박자가 세계를 멈춘 틱에는 커스텀 몹의 투사체도 멈춘다
execute if score #btHold cb matches 1 run return 0
execute as @e[tag=rlk_cmp_ar] at @s run function rlk:cm/pj/ar
execute as @e[tag=rlk_cmp_fb] at @s run function rlk:cm/pj/fb
execute as @e[tag=rlk_cmic] at @s run function rlk:cm/pj/ic
execute as @e[tag=rlk_cmp_cb] at @s run function rlk:cm/pj/cb
execute as @e[tag=rlk_cmwd] run function rlk:cm/pj/wd
