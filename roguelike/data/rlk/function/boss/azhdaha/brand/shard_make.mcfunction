# At the shard spot (floor): the gold-amber shard with the brand element inside, hovering 1 b up.
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_shard","rlk_az_shnew"],billboard:"vertical",brightness:{block:15,sky:15},teleport_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]},item:{id:"minecraft:amethyst_shard",count:1}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_az_shnew] azT 200
execute as @e[type=minecraft:item_display,tag=rlk_az_shnew] run scoreboard players operation @s azS = @a[tag=player,limit=1] azBrE
execute as @e[type=minecraft:item_display,tag=rlk_az_shnew,scores={azS=1}] run function rlk:boss/azhdaha/fx/prop/shard/1
execute as @e[type=minecraft:item_display,tag=rlk_az_shnew,scores={azS=2}] run function rlk:boss/azhdaha/fx/prop/shard/2
execute as @e[type=minecraft:item_display,tag=rlk_az_shnew,scores={azS=3}] run function rlk:boss/azhdaha/fx/prop/shard/3
execute as @e[type=minecraft:item_display,tag=rlk_az_shnew,scores={azS=4}] run function rlk:boss/azhdaha/fx/prop/shard/4
tag @e[type=minecraft:item_display,tag=rlk_az_shnew] remove rlk_az_shnew
scoreboard players operation #azShCd mb = #azClk mb
scoreboard players add #azShCd mb 300
function rlk:boss/azhdaha/fx/snd/shard_spawn
