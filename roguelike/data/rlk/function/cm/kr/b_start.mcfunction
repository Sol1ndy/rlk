scoreboard players set @s cmS 4
scoreboard players set @s cmT 16
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
particle minecraft:electric_spark ^-0.5 ^1.6 ^0.2 0.2 0.5 0.2 0.06 16
playsound minecraft:block.respawn_anchor.charge master @a ~ ~ ~ 1 1.4
