# @s = the boss at the release (lock + 9; t_combo3 51, t_spin_throw 28 hide her glaive): the thrown glaive leaves
# her hand tip first, aimed down at the locked spot (rd-sync: release 3 t before the landing).
kill @e[tag=rlk_rd_tm_flyer]
execute positioned ^-1.0 ^2.4 ^1.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_flyer"],billboard:"fixed",item_display:"none",teleport_duration:2,interpolation_duration:0,view_range:3f,width:10f,height:10f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,-4.4f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.6f,3.6f,3.6f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/glaive"}}}
execute as @e[tag=rlk_rd_tm_flyer] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_rd_tm_spot,limit=1] feet
function rlk:boss/raiden/fx/snd/glaive_sweep
