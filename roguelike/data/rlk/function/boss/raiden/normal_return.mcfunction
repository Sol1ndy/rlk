attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdRage 0
bossbar set rlk:narukami_state color yellow
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 20
