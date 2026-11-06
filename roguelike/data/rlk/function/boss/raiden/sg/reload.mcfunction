# reload (also on a datapack reload mid-fight): the weapon and the after-effect kind stay.
execute unless score @s rdWpn matches 0..1 run scoreboard players set @s rdWpn 0
execute unless score @s rdSgFx matches 0..2 run scoreboard players set @s rdSgFx 0
execute unless score @s rdSgGd matches 0.. run scoreboard players set @s rdSgGd 2
execute unless score @s rdSgEye matches 0.. run scoreboard players set @s rdSgEye 0
scoreboard players set @s rdSgFxT 0
scoreboard players set @s rdSgGs 0
scoreboard players set @s rdSgGm 0
scoreboard players set @s rdSgGp 0
scoreboard players set @s rdSgCt 0
scoreboard players set @s rdSgCk 0
scoreboard players set @s rdSgCcd 0
scoreboard players set @s rdSgRearT 0
scoreboard players set @s rdSgRearCD 0
scoreboard players set @s rdSgRearQ 0
scoreboard players set @s rdSgStun 0
scoreboard players set @s rdSgV 0
scoreboard players set @s rdSgDx 0
