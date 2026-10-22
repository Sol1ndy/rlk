# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_vajra
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/cheonsu
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/tm/vajra/drive {k:1,x:0,z:-3.5,life:304}
execute if score @s rdTime matches 12 at @s rotated as @s run function rlk:boss/raiden/tm/vajra/drive {k:2,x:3.03,z:1.75,life:298}
execute if score @s rdTime matches ..17 run return 0
execute if score @s rdTime matches 18 at @s rotated as @s run function rlk:boss/raiden/tm/vajra/drive {k:3,x:-3.03,z:1.75,life:292}
execute if score @s rdTime matches 48 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 48 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 58 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 59 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 60 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches ..83 run return 0
execute if score @s rdTime matches 84 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 84 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 94 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 95 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 96 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches 120 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 120 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches ..129 run return 0
execute if score @s rdTime matches 130 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 131 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 132 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches 156 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 156 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 166 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches ..166 run return 0
execute if score @s rdTime matches 167 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 168 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=1}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches 192 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 192 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 202 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 203 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches ..203 run return 0
execute if score @s rdTime matches 204 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=2}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches 228 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 228 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 238 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 239 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 240 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra,scores={rdTmV=3}] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches ..263 run return 0
execute if score @s rdTime matches 264 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra] at @s run function rlk:boss/raiden/fx/bolt
execute if score @s rdTime matches 264 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra] at @s run function rlk:boss/raiden/fx/snd/vajra_current
execute if score @s rdTime matches 274 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra] at @s run function rlk:boss/raiden/fx/vajra_pulse
execute if score @s rdTime matches 275 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra] at @s run function rlk:boss/raiden/hazard/new {k:5,a:2000,b:800000,c:1400,d:0,e:-1000,f:32,tol:300,tell:1,dmg:14,life:34,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:24,sm:0,go:2,sp:-1,snd:1,nd:0,jp:1,det:0,lf:0,fv:0}
execute if score @s rdTime matches 276 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_vajra] at @s run function rlk:boss/raiden/fx/snd/vajra_ring
execute if score @s rdTime matches 310 at @s rotated as @s run function rlk:boss/raiden/finish
