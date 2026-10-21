execute if score @s rdTime matches 0 at @s rotated as @s run scoreboard players set @s rdSgV 0
execute if score @s rdTime matches 0 at @s rotated as @s run execute if entity @e[tag=rlk_body,distance=..6,limit=1] run scoreboard players set @s rdSgV 1
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/noemyeong
execute if score @s rdTime matches 0 if score @s rdSgV matches 0 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^5.5 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 0 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/play/iai_near
execute if score @s rdTime matches 12 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 12 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 12 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/iai_dash
execute if score @s rdTime matches 12 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:10000,b:1500,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:14,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^9 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgpt","rlk_rd_tmp","rlk_raiden_aux","rlk_room"]}
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/clamp_pt
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned as @e[tag=rlk_rd_sgpt,limit=1] run function rlk:boss/raiden/hazard/new {k:2,a:0,b:4000,c:940,d:342,e:18490000,f:0,tol:300,tell:18,dmg:13,life:29,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:4,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 18 if score @s rdSgV matches 0 at @s rotated as @s run kill @e[tag=rlk_rd_sgpt]
execute if score @s rdTime matches 28 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 29 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 30 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 31 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 32 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 33 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 34 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 35 if score @s rdSgV matches 0 at @s rotated as @s run execute positioned ^ ^ ^1.125 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 28 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/fx/snd/rush
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run execute positioned ~ ~1.2 ~ run execute positioned ^ ^ ^0.6 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:9000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:14,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 10 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:4000,b:1000,c:0,d:0,e:0,f:0,tol:300,tell:18,dmg:13,life:29,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 40 if score @s rdSgV matches 1 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 66 if score @s rdSgV matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
