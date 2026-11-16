execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/guard
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/mock
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/guard_on
execute if score @s rdTime matches 1..159 at @s rotated as @s run execute if score @s rdSgCt matches 1.. run function rlk:boss/raiden/sg/counter_tick
execute if score @s rdTime matches 1..159 at @s rotated as @s run execute if score @s rdSgCt matches 0 if score @s rdRigC matches 11 if score @s rdRigT matches 6.. run function rlk:boss/raiden/rig/play/guard
execute if score @s rdTime matches 160 at @s rotated as @s run function rlk:boss/raiden/sg/guard_off
execute if score @s rdTime matches 160 at @s rotated as @s run execute if score @s rdSgGp matches ..3 run function rlk:boss/raiden/finish
execute if score @s rdTime matches 160 if score @s rdSgGp matches 4.. at @s rotated as @s run function rlk:boss/raiden/rig/play/karatake
execute if score @s rdTime matches 160 if score @s rdSgGp matches 4.. at @s rotated as @s run function rlk:boss/raiden/line/end_it
execute if score @s rdTime matches 160 if score @s rdSgGp matches 4.. at @s rotated as @s run function rlk:boss/raiden/fx/blink_out
execute if score @s rdTime matches 160 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 161 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 162 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 163 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 164 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 165 if score @s rdSgGp matches 4.. at @s rotated as @s run execute positioned ^ ^ ^-1 if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdTime matches 170 if score @s rdSgGp matches 4.. at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 170 if score @s rdSgGp matches 4.. at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 170 if score @s rdSgGp matches 4.. at @s rotated as @s run function rlk:boss/raiden/fx/snd/iai_charge
execute if score @s rdTime matches 170 if score @s rdSgGp matches 4.. at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:14000,b:1500,c:0,d:0,e:0,f:0,tol:300,tell:20,dmg:24,life:31,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 192 at @s rotated as @s run function rlk:boss/raiden/finish
