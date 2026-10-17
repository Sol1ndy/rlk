# pull tick 40 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.465 ^1.296 ^-1.276 0.08 0.08 0.08 0 2 force @a[tag=player]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc]
# Pull clip over: a refused pull (#gp4Ok 0) ends the pattern here (no swings, nothing to show).
execute if score #gp4Ok mb matches 0 run function rlk:mboss/guardian/p/pull/scr_end
execute if score #gp4Ok mb matches 0 run scoreboard players set #gdPLen mb 40
execute if score #gp4Ok mb matches 0 run function rlk:mboss/guardian/p/end
