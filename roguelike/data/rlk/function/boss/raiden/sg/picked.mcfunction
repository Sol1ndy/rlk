# core choose after the test hooks (phase 0): the move leaves its weapon bag; guard spacing; eye queue;
# rear-check cooldown; the rig weapon follows rdWpn.
execute if score @s rdWpn matches 0 if score @s rdPat matches 3 run scoreboard players set #rdSgB0_3 rd 0
execute if score @s rdWpn matches 0 if score @s rdPat matches 8 run scoreboard players set #rdSgB0_8 rd 0
execute if score @s rdWpn matches 0 if score @s rdPat matches 2 run scoreboard players set #rdSgB0_2 rd 0
execute if score @s rdWpn matches 0 if score @s rdPat matches 5 run scoreboard players set #rdSgB0_5 rd 0
execute if score @s rdWpn matches 0 if score @s rdPat matches 9 run scoreboard players set #rdSgB0_9 rd 0
execute if score @s rdWpn matches 0 if score @s rdPat matches 10 run scoreboard players set #rdSgB0_10 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 1 run scoreboard players set #rdSgB1_1 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 21 run scoreboard players set #rdSgB1_21 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 22 run scoreboard players set #rdSgB1_22 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 23 run scoreboard players set #rdSgB1_23 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 24 run scoreboard players set #rdSgB1_24 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 9 run scoreboard players set #rdSgB1_9 rd 0
execute if score @s rdWpn matches 1 if score @s rdPat matches 10 run scoreboard players set #rdSgB1_10 rd 0
scoreboard players add @s rdSgGd 1
execute if score @s rdPat matches 9 run scoreboard players set @s rdSgGd 0
execute if score @s rdPat matches 10 run scoreboard players set @s rdSgEye 2
execute if score @s rdPat matches 4 run scoreboard players set @s rdSgEye 0
execute if score @s rdPat matches 25..26 run scoreboard players set @s rdSgRearCD 300
execute if score @s rdPat matches 25..26 run scoreboard players set @s rdSgRearT 0
scoreboard players set @s rdSgV 0
execute unless score @s rdWpn = @s rdRigW run function rlk:boss/raiden/sg/look
