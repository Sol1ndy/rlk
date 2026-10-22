execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s run function rlk:boss/raiden/hazard/new {k:3,a:8000,b:750,c:0,d:0,e:0,f:0,tol:300,tell:12,dmg:8,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:7,sm:3,go:0,sp:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.2
