execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/switch_sword
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/command
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/switch_hoop
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/prop/hoop
execute if score @s rdTime matches 0 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_sg
execute if score @s rdTime matches 0 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
execute if score @s rdTime matches 0 at @s rotated as @s run execute positioned ^ ^ ^1 run function rlk:boss/raiden/hazard/new {k:1,a:6000,b:0,c:0,d:0,e:39690000,f:0,tol:300,tell:20,dmg:16,life:31,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/rig/prop/vortex
execute if score @s rdTime matches 6 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_sg
execute if score @s rdTime matches 6 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
execute if score @s rdTime matches 18 at @s rotated as @s run kill @e[tag=rlk_rd_prop_vortex,tag=rlk_rd_sg]
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/fx/switch_burst
execute if score @s rdTime matches 20 at @s rotated as @s run kill @e[tag=rlk_rd_prop_hoop,tag=rlk_rd_sg]
execute if score @s rdTime matches 22 at @s rotated as @s run scoreboard players set @s rdWpn 0
execute if score @s rdTime matches 34 at @s rotated as @s run scoreboard players set @s rdSgFx 1
execute if score @s rdTime matches 34 at @s rotated as @s run scoreboard players set @s rdSgFxT 0
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/finish
