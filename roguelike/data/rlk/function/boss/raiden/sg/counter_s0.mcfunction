# Sword counter: black line (cue) + shield block, spin 12 (disk r 3), floor bolts 24 (rect 8 x 1.5, aimed 12),
# lunge 40 (rect 8 x 2, re-aimed 28).
function rlk:boss/raiden/rig/play/counter_sword
function rlk:boss/raiden/fx/counter_cue
playsound minecraft:item.shield.block hostile @a[tag=player] ~ ~ ~ 1 1.4 0.2
function rlk:boss/raiden/hazard/new {k:1,a:3000,b:0,c:0,d:0,e:10890000,f:0,tol:300,tell:12,dmg:8,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
