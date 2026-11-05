# {kb} (api.disc; @s = the body, at it): one A7 moon disc (PLAN §4.5): a blade projectile (#pjShape 1, half width
# 1.4 b, 1.8 b/t asked = 2.0 b/t flown (0.25 b sub-steps rounded up), life 16 t, wall stop),
# 0.9 b over the floor (the blade rows cover 0 .. 1.65 b: a jump does not clear it), aimed at the player's position now
# (no homing), T2 Electro, kb; one card: summoned 1 b in front of her, then rotated (pitch 0), then launched and
# dressed (kit fx/prop/disc; else a flat purple pane). Never counts for the shield.
kill @e[type=minecraft:item_display,tag=rlk_hr_gdn]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1 positioned ~ 201.9 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_disc","rlk_hr_gdn"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:purple_stained_glass_pane",count:1},transformation:{left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.8f,2.8f,0.2f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_gdn] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_gdn] run function rlk:boss/scarlet/g/disc/tag
scoreboard players set #pjEl mb 3
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
$scoreboard players set #pjKB mb $(kb)
execute as @e[type=minecraft:item_display,tag=rlk_hr_gdn] at @s rotated as @s run function rlk:mboss/pj/launch {spd:20,life:16,dmg:42,hr:14}
tag @e[type=minecraft:item_display,tag=rlk_hr_gdn] remove rlk_hr_gdn
