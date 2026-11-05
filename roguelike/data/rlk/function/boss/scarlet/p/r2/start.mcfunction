# R2 월륜 일섬 (P2: the moon disc after the yellow tell; S4, p_ghost.py): pattern tick 0 (@s = the body, at it; clock #pt hr).
scoreboard players set #done hr 0
# the second disc at <= 30 % of her max HP (#r2_two 1): 100 x HP <= 30 x max HP
scoreboard players set #r2_two hr 0
scoreboard players operation #r2_a hr = @s mhpC
scoreboard players operation #r2_a hr *= #c100 hr
scoreboard players operation #r2_b hr = @s mhpM
scoreboard players set #r2_c hr 30
scoreboard players operation #r2_b hr *= #r2_c hr
execute if score #r2_a hr <= #r2_b hr run scoreboard players set #r2_two hr 1
function rlk:boss/scarlet/rig/play/a7_tell
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/back1
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
