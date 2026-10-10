execute if score @s dashUpN matches 1.. run return 0
scoreboard players set #dblk tmp 0
$execute if score @s dashDZ matches 1.. positioned ~ ~1 ~$(dz) run function rlk:player/dash_chk_zp
$execute if score @s dashDZ matches ..-1 positioned ~ ~1 ~$(dz) run function rlk:player/dash_chk_zn
$execute if score #dblk tmp matches 0 run tp @e[tag=rlk_body,limit=1] ~ ~1 ~$(dz)
execute if score #dblk tmp matches 0 run scoreboard players set @s dashUpN 1
