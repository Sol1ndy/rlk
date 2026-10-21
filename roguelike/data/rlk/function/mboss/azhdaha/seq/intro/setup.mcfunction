# The intro dressing (plan 5 E, [v1] I): 6 seal steles r 8 around the spawn (facing the centre), the gold glyph
# prism (UUID 0x80) standing at the centre, the floor glyph circle (decor). Per-fight entities (rlk_mb_aux).
kill @e[tag=rlk_mb_az_seal]
execute in minecraft:overworld positioned 324 201 1.072 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s0"],Rotation:[30f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute in minecraft:overworld positioned 328 201 8 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s1"],Rotation:[90f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute in minecraft:overworld positioned 324 201 14.928 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s2"],Rotation:[150f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute in minecraft:overworld positioned 316 201 14.928 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s3"],Rotation:[-150f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute in minecraft:overworld positioned 312 201 8 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s4"],Rotation:[-90f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute in minecraft:overworld positioned 316 201 1.072 run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_s5"],Rotation:[-30f,0f],billboard:"fixed",brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_seal] run function rlk:mboss/azhdaha/fx/prop/seal_stele
execute in minecraft:overworld positioned 320 201 8 run kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism]
execute in minecraft:overworld positioned 320 201 8 run summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,128],Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_seal","rlk_mb_az_seal_prism"],billboard:"fixed",brightness:{block:15,sky:15},item:{id:"minecraft:yellow_stained_glass",count:1}}
execute in minecraft:overworld positioned 320 201 8 run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism] run function rlk:mboss/azhdaha/fx/prop/seal_prism
execute in minecraft:overworld positioned 320 201 8 run function rlk:mboss/azhdaha/fx/tele/glyph_circle {r:90,tell:20,hold:92}
