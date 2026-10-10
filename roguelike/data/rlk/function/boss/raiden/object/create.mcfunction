# At the desired ground point, as boss; kinds: 1 eye,2 illusion,3 flower,4 stake.
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object","rlk_rd_objnew","rlk_mob","rlk_mapv"],NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,IsBaby:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjKind $(kind)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjId $(id)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjHP $(hp)
scoreboard players set @e[tag=rlk_rd_objnew] rdHitCD 0
scoreboard players set @e[tag=rlk_rd_objnew] rdOAge 0
scoreboard players set @e[tag=rlk_rd_objnew] rdReal 0
scoreboard players set @e[tag=rlk_rd_objnew] mhpC 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhpM 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhp0 1000000
scoreboard players set @e[tag=rlk_rd_objnew] xpDrop 0
scoreboard players operation @e[tag=rlk_rd_objnew] mlv = @e[tag=rlk_raiden,limit=1] mlv
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:max_health base set 1024
execute as @e[tag=rlk_rd_objnew] run data modify entity @s Health set value 1024f
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:attack_damage base set 0
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:knockback_resistance base set 1
team join rlk_cam @e[tag=rlk_rd_objnew]
$summon minecraft:item_display ~ ~$(y) ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_objvisual","rlk_rd_visnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/$(model)"}},item_display:"none",brightness:{sky:15,block:15},view_range:2f,transformation:{translation:[0f,0f,0f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
$scoreboard players set @e[tag=rlk_rd_visnew] rdObjId $(id)
tag @e[tag=rlk_rd_visnew] remove rlk_rd_visnew
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=4}] run tag @s remove rlk_mob
execute as @e[tag=rlk_rd_objnew] at @s run function rlk:boss/raiden/object_vfx/create
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=3}] at @s run function rlk:boss/raiden/orb/create
tag @e[tag=rlk_rd_objnew] remove rlk_rd_objnew
