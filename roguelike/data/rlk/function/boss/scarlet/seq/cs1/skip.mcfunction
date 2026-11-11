# The CS1 skip (@s = the body; hr_design §3.2): the black falls; under it the line and the petals go, she stands on her
# mark facing the actor with the sword sheathed, the hat on and the bottle gone (the state of tick 566), her clip is
# moved to tick 565 (the rig shows 566 at the next rig/tick: the clip keys every part there), her model put at the
# mark now (RIG_NOW), both cameras made anew on S10; seq/cs1/skipgo then sets #sq to 565. Line 15, line 16 and the
# slash follow.
function rlk:boss/scarlet/fx/hud/clear
data modify storage rlk:mboss camtx.line set value {text:"",background:0}
function rlk:mboss/cam/text
function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:20,out:6}
scoreboard players set @a[tag=player] hudHold 2
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp]
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/cs1/m/mark
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
function rlk:boss/scarlet/rig/look/sword/sheathed
function rlk:boss/scarlet/rig/look/hat/worn
function rlk:boss/scarlet/rig/look/scabbard/hip
function rlk:boss/scarlet/rig/look/props/none
function rlk:boss/scarlet/rig/look/face/calm
scoreboard players set @s hrRigT 565
execute unless score #sq_cx hr matches 1 run function rlk:mboss/cam/kill
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-0.1 ^1.38 ^0.95
execute unless score #sq_cx hr matches 1 as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.6 ^0
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
execute unless score #sq_cx hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute unless score #sq_cx hr matches 1 as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-0.1 ^1.38 ^0.95
execute unless score #sq_cx hr matches 1 as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.6 ^0
execute unless score #sq_cx hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
execute unless score #sq_cx hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute unless score #sq_cx hr matches 1 as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute unless score #sq_cx hr matches 1 run scoreboard players set #mbCamId mb 1
