# The unparriable-attack warning (combat overhaul C; the original's yellow flash, video_notes 1.6): a gold sphere-ring with a
# long horizontal flare on the boss's chest, bright then fading (player/def/fx/glint), and a chime. Once per #npGap tmp ticks
# (a volley warns once); never while a cutscene runs; a module that draws its own warnings sets #mbNpOwn mb 1.
execute if score #mbNpOwn mb matches 1 run return 0
execute if score #mbCine mb matches 1 run return 0
execute store result score #npNow mb run time query gametime
scoreboard players operation #t mb = #npNow mb
scoreboard players operation #t mb -= #mbNpAt mb
execute if score #t mb < #npGap tmp run return 0
scoreboard players operation #mbNpAt mb = #npNow mb
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s anchored eyes positioned ^ ^-0.35 ^ run function rlk:player/def/fx/glint
