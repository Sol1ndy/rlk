# The intro skip (@s = the body; hr_design §3.1, v_brief VC 8): the black falls; under it the intro is cleared (the line,
# the wind, the rock and the props, a move in progress, the petal), she stands at f 6.5 facing the actor (the
# landing's place) and her model with her (RIG_NOW: the rig's own follow runs in the tick's stale position, so without
# it she stayed on the rock until the fight began), both cameras are made anew on I18; seq/intro/skipgo then sets #sq to
# 1289 and the next tick plays intro_end from its tick 0. The actor shows its tick 1290 by itself (#cavT cine follows
# #sq). Line 11 is typed on the camera text, under the black until that has faded.
function rlk:boss/scarlet/fx/hud/clear
data modify storage rlk:mboss camtx.line set value {text:"",background:0}
function rlk:mboss/cam/text
function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:20,out:6}
stopsound @a[tag=player] * minecraft:item.elytra.flying
execute if data storage rlk:mboss {look_hr_field:"moon"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
execute if data storage rlk:mboss {look_hr_field:"crimson"} as @e[type=minecraft:item_display,tag=rlk_hr_deco_moon_halo] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p2"}
scoreboard players set @a[tag=player] hudHold 2
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
function rlk:mboss/mv/stop
execute positioned 884.0 201 5.0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^6.5 run tp @s ~ ~ ~
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
execute unless score #sq_cx hr matches 1 run function rlk:mboss/cam/kill
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-0.15 ^1.95 ^1.9 facing ^0 ^1.55 ^0
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
execute unless score #sq_cx hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-0.15 ^1.95 ^1.9 facing ^0 ^1.55 ^0
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
execute unless score #sq_cx hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute unless score #sq_cx hr matches 1 run scoreboard players set #mbCamId mb 1
