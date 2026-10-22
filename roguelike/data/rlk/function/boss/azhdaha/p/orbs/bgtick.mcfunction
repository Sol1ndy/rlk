# bg slot L clock #azBgLT: grow 0-9 (harmless), orbit until #aq31E (600; refresh moves it), fade 10 t, end.
scoreboard players set #aq31K mb 36000
execute if score #azBgLT mb matches ..9 run function rlk:boss/azhdaha/p/orbs/grow
execute if score #azBgLT mb matches 1 as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d] run data merge entity @s {start_interpolation:0,interpolation_duration:9,transformation:{scale:[2.6f,2.6f,2.6f]}}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p31o] run function rlk:boss/azhdaha/orb/step
execute store result score #aq31Y mb run data get entity @s Rotation[0] 100
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p31o0,limit=1] at @s run function rlk:boss/azhdaha/p/orbs/band
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d0,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_p31o0,limit=1] run function rlk:boss/azhdaha/p/orbs/prop
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p31o1,limit=1] at @s run function rlk:boss/azhdaha/p/orbs/band
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d1,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_p31o1,limit=1] run function rlk:boss/azhdaha/p/orbs/prop
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p31o2,limit=1] at @s run function rlk:boss/azhdaha/p/orbs/band
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d2,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_p31o2,limit=1] run function rlk:boss/azhdaha/p/orbs/prop
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p31o3,limit=1] at @s run function rlk:boss/azhdaha/p/orbs/band
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d3,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_p31o3,limit=1] run function rlk:boss/azhdaha/p/orbs/prop
# the hit cue (the group was marked this tick)
scoreboard players set #aq31N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzHit matches 1 run scoreboard players set #aq31N mb 1
execute if score #aq31N mb matches 1 unless score #aq31W mb matches 1 at @e[tag=rlk_body,limit=1] run function rlk:boss/azhdaha/fx/snd/orb_hit
scoreboard players operation #aq31W mb = #aq31N mb
execute if score #azBgLT mb matches 10.. if score #azBgLT mb < #aq31E mb run function rlk:boss/azhdaha/p/orbs/amb
execute if score #azBgLT mb = #aq31E mb run function rlk:boss/azhdaha/p/orbs/fade
scoreboard players operation #aq31X mb = #aq31E mb
scoreboard players add #aq31X mb 10
execute if score #azBgLT mb >= #aq31X mb run function rlk:boss/azhdaha/p/orbs/end
