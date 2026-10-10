scoreboard players set @s pmWantW 1
execute if score #charN tmp matches 5 if score @s arM matches 1.. run scoreboard players set @s pmWantW 2
execute if score #charN tmp matches 3 run scoreboard players set @s pmWantW 3
execute if score #charN tmp matches 3 if score @s skM matches 1.. run scoreboard players set @s pmWantW 4
execute unless score @s pmWeapon = @s pmWantW run function rlk:char/motion/loco/weapon_set
