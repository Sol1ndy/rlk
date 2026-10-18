# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# @s = anchor (the body), at it, rotated as it: kills old parts, summons the stand-in in the cruise pose.
function rlk:mboss/fieldgen/rig_stub/init
function rlk:mboss/fieldgen/rig_stub/kill
summon minecraft:item_display ^0 ^4.5 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_ring"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[7f,7f,7f]},item:{id:"minecraft:clock",count:1}}
summon minecraft:item_display ^0 ^4.6 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_core"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f]},item:{id:"minecraft:gold_block",count:1}}
summon minecraft:item_display ^0 ^6.1 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_halo"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f]},item:{id:"minecraft:yellow_stained_glass_pane",count:1}}
summon minecraft:item_display ^0 ^2.65 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_pend"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.4f,2.2f,1.4f]},item:{id:"minecraft:lightning_rod",count:1}}
summon minecraft:item_display ^3.3 ^4.15 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_medal_e"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
summon minecraft:item_display ^-3.3 ^4.15 ^0 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fgs","rlk_mb_fg_medal_g"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
scoreboard players set @s fgRigC 0
scoreboard players set @s fgRigT -1
scoreboard players set @s fgRigF 1
scoreboard players set @s fgRigL 0
scoreboard players set @s fgRigK 0
scoreboard players set @s fgRigY 0
scoreboard players set @s fgRigV 0
