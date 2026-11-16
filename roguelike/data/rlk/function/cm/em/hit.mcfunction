scoreboard players set @s c2T2 1
scoreboard players set #c3EmHit tmp 1
execute unless score #c3emstab snd matches 1 run function rlk:cm/c3/snd/emstab
scoreboard players operation #cmDmg tmp = #c3D_em tmp
function rlk:cm/hit_me
