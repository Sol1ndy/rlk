kill @e[tag=rlk_doll]
summon minecraft:armor_stand ~ ~ ~ {Tags:["rlk_doll","rlk_pet","rlk_isn"],Invulnerable:1b,NoGravity:1b,Small:1b,ShowArms:1b,NoBasePlate:1b,DisabledSlots:4144959,equipment:{head:{id:"minecraft:carved_pumpkin",count:1},mainhand:{id:"minecraft:shears",count:1}}}
execute as @e[tag=rlk_isn] run rotate @s ~ 0
scoreboard players operation @e[tag=rlk_isn] life = #dollDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:block.wool.place master @a ~ ~ ~ 1 1.2
