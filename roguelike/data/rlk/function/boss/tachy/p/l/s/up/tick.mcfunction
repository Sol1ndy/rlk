# L stage up: one tick (#l_c 1..).
execute if score #l_c tk matches 4 at @s positioned ~ 214 ~ run function rlk:mboss/mv/glide {t:12}
execute if score #l_c tk matches 8 run tag @s add rlk_mb_inv
execute if score #l_c tk matches 16 run return run function rlk:boss/tachy/p/l/s/up/k/16
