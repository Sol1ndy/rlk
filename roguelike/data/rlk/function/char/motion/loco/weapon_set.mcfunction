execute if score @s pmWantW matches 1 run function rlk:char/motion/loco/weapon/spear
execute if score @s pmWantW matches 2 run function rlk:char/motion/loco/weapon/scythe
execute if score @s pmWantW matches 3 run function rlk:char/motion/loco/weapon/sword
execute if score @s pmWantW matches 4 run function rlk:char/motion/loco/weapon/cryo_sword
scoreboard players operation @s pmWeapon = @s pmWantW
