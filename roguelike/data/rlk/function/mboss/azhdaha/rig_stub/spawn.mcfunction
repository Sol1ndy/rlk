# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# @s = anchor (the body husk on the floor), at it, rotated as it: kills old parts, summons the stand-in,
# queues idle, re-applies the stored looks and the visibility state.
function rlk:mboss/azhdaha/rig_stub/init
function rlk:mboss/azhdaha/rig_stub/kill
summon minecraft:item_display ^0 ^2.9 ^-0.3 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","rlk_mb_azs","rlk_mb_az_sbody"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:30f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[5.4f,3.2f,8.6f]},item:{id:"minecraft:tuff",count:1}}
summon minecraft:item_display ^0 ^1.6 ^4.6 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","rlk_mb_azs","rlk_mb_az_shead"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:30f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,2f,2.6f]},item:{id:"minecraft:polished_blackstone",count:1}}
summon minecraft:item_display ^0 ^1.6 ^-10.3 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","rlk_mb_azs","rlk_mb_az_stail"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:30f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,11f]},item:{id:"minecraft:stripped_jungle_log",count:1}}
summon minecraft:item_display ^0 ^2.15 ^5.95 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","rlk_mb_azs","rlk_mb_az_seyes"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{block:13,sky:15},view_range:3f,width:30f,height:12f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.4f,0.25f,0.3f]},item:{id:"minecraft:redstone_block",count:1}}
execute unless score @s azRigLegs matches 0..2 run scoreboard players set @s azRigLegs 0
execute unless score @s azRigTail matches 0..2 run scoreboard players set @s azRigTail 0
execute unless score @s azRigState matches 0..2 run scoreboard players set @s azRigState 0
scoreboard players set @s azRigC 1000
scoreboard players set @s azRigT -1
scoreboard players set @s azRigF 0
function rlk:mboss/azhdaha/rig_stub/look_apply
