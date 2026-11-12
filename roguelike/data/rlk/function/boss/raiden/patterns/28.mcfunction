execute if score @s rdTime matches 0 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/rig/play/switch_polearm
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/line/musang
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/fx/switch_hoop
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/rig/prop/hoop
execute if score @s rdTime matches 14 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_sg
execute if score @s rdTime matches 14 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/rig/prop/vortex
execute if score @s rdTime matches 14 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_sg
execute if score @s rdTime matches 14 at @s rotated as @s run tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:1,a:5000,b:0,c:0,d:0,e:28090000,f:0,tol:300,tell:20,dmg:16,life:31,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 30 at @s rotated as @s run execute positioned ~ ~1.6 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 32 at @s rotated as @s run kill @e[tag=rlk_rd_prop_vortex,tag=rlk_rd_sg]
execute if score @s rdTime matches 34 at @s rotated as @s run function rlk:boss/raiden/fx/switch_burst
execute if score @s rdTime matches 34 at @s rotated as @s run kill @e[tag=rlk_rd_prop_hoop,tag=rlk_rd_sg]
execute if score @s rdTime matches 36 at @s rotated as @s run scoreboard players set @s rdWpn 1
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdSgFx 2
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdSgFxT 0
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/finish
