kill @e[tag=rlk_pot]
execute rotated ~ 0 run summon minecraft:item_display ~ ~0.5 ~ {Tags:["rlk_pot","rlk_potnew"],brightness:{sky:15,block:15},item:{id:"minecraft:cauldron",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
execute rotated ~ 0 as @e[tag=rlk_potnew] run rotate @s ~ ~
scoreboard players set @e[tag=rlk_potnew] life 0
scoreboard players operation @e[tag=rlk_potnew] pcVal = #potN tmp
tag @e[tag=rlk_potnew] remove rlk_potnew
playsound minecraft:block.anvil.place master @a ~ ~ ~ 0.3 1.6
