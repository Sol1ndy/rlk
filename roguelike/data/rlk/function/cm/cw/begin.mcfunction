# 영창 시작: 물 구슬이 머리 위로, 빛남
scoreboard players set @s cmS 1
scoreboard players operation @s c3H = #c3Hi_cw tmp
execute as @e[tag=rlk_cw_orb,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:6737151}
execute unless score #c3cwcast snd matches 1 run function rlk:cm/c3/snd/cwcast
execute unless score #c3cwsplash snd matches 1 run function rlk:cm/c3/snd/cwsplash
