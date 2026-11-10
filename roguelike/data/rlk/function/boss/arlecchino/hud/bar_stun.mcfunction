scoreboard players operation #buSub bu = #stun_t kn
scoreboard players set #buSubMax bu 160
scoreboard players set #buSubCol bu 2
# the balance groggy (combat overhaul lane B) is a 100 t stun
execute if score @s grgT matches 1.. run scoreboard players set #buSubMax bu 100
