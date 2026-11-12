# End of the transformation: the Tenma phase with the full armour (the shield takes over from the phase-1 tag).
attribute @s minecraft:scale base set 2.2
scoreboard players set @s rdPhase 2
tag @s remove rlk_rd_armoured
scoreboard players set @s rdShield 750
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdPTime 0
scoreboard players set @s rdTurns 0
scoreboard players set @s rdHitCD 0
scoreboard players set @s rdTmCD 0
scoreboard players set @s rdTmChain 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 14
