# new cicin (@s, at @s)
function rlk:cm/init
scoreboard players set @s c2eOw 0
execute store result score @s c2eA run random value 0..359
scoreboard players set @s c2eF 0
scoreboard players set @s cmCd 50
function rlk:cm/ci/rig/create
