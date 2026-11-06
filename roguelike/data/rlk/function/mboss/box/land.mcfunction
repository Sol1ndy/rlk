# @s = box display at rest, at @s (centre 0.55 b above the floor): thud, dust puff and gold burst, a short
# squash (bottom kept on the floor; it starts 1 t later, when the client has finished the last interpolated fall
# step, and box/fall springs it back at 17), then the clickable room object around it (the display joins its group).
particle minecraft:poof ~ ~-0.5 ~ 0.45 0.02 0.45 0.03 12
particle minecraft:dust{color:[1.0f,0.84f,0.36f],scale:1.6f} ~ ~-0.45 ~ 0.6 0.03 0.6 0 16
particle minecraft:end_rod ~ ~0.1 ~ 0.1 0.1 0.1 0.08 8
playsound minecraft:block.chest.close block @a[tag=player] ~ ~ ~ 0.8 0.7
playsound minecraft:block.wood.fall block @a[tag=player] ~ ~ ~ 1 0.7
playsound minecraft:block.anvil.land block @a[tag=player] ~ ~ ~ 0.15 1.6
data merge entity @s {start_interpolation:1,interpolation_duration:2,transformation:{translation:[0f,-0.099f,0f],scale:[1.232f,0.902f,1.232f]}}
tag @s add rlk_new
execute positioned ~ ~-0.55 ~ run function rlk:room/obj/k_mbox
