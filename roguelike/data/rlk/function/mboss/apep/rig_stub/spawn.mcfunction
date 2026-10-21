# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# @s = anchor, at it: kills old parts, summons the stand-in, keeps the stored channels (form, stance, state,
# park, brightness), queues the idle of the form.
function rlk:mboss/apep/rig_stub/init
function rlk:mboss/apep/rig_stub/kill
execute rotated as @s rotated ~ 0 run summon minecraft:item_display ^0 ^2.6 ^-0.4 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_aps","rlk_mb_ap_sbody"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:24f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[4.2f,2.4f,6f]},item:{id:"minecraft:moss_block",count:1}}
execute rotated as @s rotated ~ 0 run summon minecraft:item_display ^0 ^3.4 ^2.4 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_aps","rlk_mb_ap_shead"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:24f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[2.4f,2.4f,2.4f]},item:{id:"minecraft:pitcher_plant",count:1}}
execute rotated as @s rotated ~ 0 run summon minecraft:item_display ^0.6 ^1.4 ^-7.4 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_aps","rlk_mb_ap_stail"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:24f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1f,9f]},item:{id:"minecraft:stripped_mangrove_log",count:1}}
execute unless score @s apRigForm matches 0.. run scoreboard players set @s apRigForm 0
execute unless score @s apRigStance matches 0.. run scoreboard players set @s apRigStance 0
execute unless score @s apRigState matches 0.. run scoreboard players set @s apRigState 0
execute unless score @s apRigPark matches 0.. run scoreboard players set @s apRigPark 0
execute unless score @s apRigBright matches 0.. run scoreboard players set @s apRigBright 0
execute unless score @s apRigFace matches 0.. run scoreboard players set @s apRigFace 0
execute unless score @s apRigCore matches 0.. run scoreboard players set @s apRigCore 0
execute unless score @s apRigGlow matches 0.. run scoreboard players set @s apRigGlow 0
execute unless score @s apRigTint matches 0.. run scoreboard players set @s apRigTint 0
execute unless score @s apRigHands matches 0.. run scoreboard players set @s apRigHands 0
scoreboard players set @s apRigC 1001
execute if score @s apRigForm matches 1 run scoreboard players set @s apRigC 1023
scoreboard players set @s apRigT -1
scoreboard players set @s apRigF 0
function rlk:mboss/apep/rig_stub/look_apply
