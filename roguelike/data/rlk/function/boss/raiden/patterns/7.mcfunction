execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/movement/depart
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/rig/play/musou
execute if score @s rdTime matches 0 at @s rotated as @s run function rlk:boss/raiden/line/calm
execute if score @s rdTime matches 0 at @s rotated as @s run scoreboard players set @s rdBlink 24
execute if score @s rdTime matches 0 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~
execute if score @s rdTime matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/movement/arrive
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/sg/musou_orbs
execute if score @s rdTime matches 20 at @s rotated as @s run execute positioned ~ ~2.4 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 30 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=0}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 30 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=0}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 50 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=0}]
execute if score @s rdTime matches 38 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=1}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 38 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=1}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 58 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=1}]
execute if score @s rdTime matches 46 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=2}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 46 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=2}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 66 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=2}]
execute if score @s rdTime matches 54 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=3}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 54 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=3}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 74 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=3}]
execute if score @s rdTime matches 62 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=4}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 62 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=4}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 82 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=4}]
execute if score @s rdTime matches 70 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=5}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 70 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=5}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 90 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=5}]
execute if score @s rdTime matches 78 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=6}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 78 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=6}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 98 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=6}]
execute if score @s rdTime matches 86 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=7}] at @s run function rlk:boss/raiden/hazard/new {k:1,a:4000,b:0,c:0,d:0,e:18490000,f:0,tol:300,tell:20,dmg:10,life:31,ev:10,max:1,grp:0,dk:3,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 86 at @s rotated as @s run execute as @e[tag=rlk_rd_sgorb,scores={rdSgDx=7}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2
execute if score @s rdTime matches 106 at @s rotated as @s run kill @e[tag=rlk_rd_sgorbp,scores={rdSgDx=7}]
execute if score @s rdTime matches 110 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/musou_dark {life:50}
execute if score @s rdTime matches 110 at @s rotated as @s run function rlk:boss/raiden/line/sever_one
execute if score @s rdTime matches 110 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~1.5 ~ run function rlk:boss/raiden/fx/crystal
execute if score @s rdTime matches 110 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:19000,b:0,c:0,d:0,e:372490000,f:0,tol:300,tell:20,dmg:30,life:31,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdTime matches 130 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/musou_slash
execute if score @s rdTime matches 136 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 30 0 positioned ^ ^ ^-9 run function rlk:boss/raiden/fx/crystal_line {len:18}
execute if score @s rdTime matches 144 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 150 0 positioned ^ ^ ^-9 run function rlk:boss/raiden/fx/crystal_line {len:18}
execute if score @s rdTime matches 152 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 270 0 positioned ^ ^ ^-9 run function rlk:boss/raiden/fx/crystal_line {len:18}
execute if score @s rdTime matches 160 at @s rotated as @s run execute positioned ~ ~1.6 ~ run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 166 at @s rotated as @s run function rlk:boss/raiden/finish
