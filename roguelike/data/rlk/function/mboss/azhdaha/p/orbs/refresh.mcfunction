# Transition 2 with live orbs (core cast host, roar_low): full life again, no new orbs; a fading orb grows back.
scoreboard players operation #aq31E mb = #azBgLT mb
scoreboard players add #aq31E mb 600
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[2.6f,2.6f,2.6f]}}
function rlk:mboss/azhdaha/fx/snd/orb_spawn
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d] at @s run function rlk:mboss/azhdaha/fx/p/splash
