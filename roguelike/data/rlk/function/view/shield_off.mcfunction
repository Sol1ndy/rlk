# 보호막이 깨지거나 끝남: 울타리를 없애고 깨지는 반짝임
execute at @e[tag=rlk_shfx,limit=1] run particle minecraft:block{block_state:"minecraft:glass"} ~ ~0.4 ~ 0.6 0.3 0.6 0.1 16
execute at @e[tag=rlk_shfx,limit=1] unless score #k62 snd matches 1 run function rlk:snd/f224
kill @e[tag=rlk_shfx]
