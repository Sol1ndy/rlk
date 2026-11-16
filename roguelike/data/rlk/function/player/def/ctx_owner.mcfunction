# @s = 커스텀 몹의 투사체(cmId = 주인). 주인 두뇌에 rlk_hc_atk
scoreboard players operation #hcId tmp = @s cmId
execute as @e[type=!minecraft:player,tag=rlk_cmb] if score @s cmId = #hcId tmp run tag @s add rlk_hc_atk
