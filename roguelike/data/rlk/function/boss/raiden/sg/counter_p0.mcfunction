# Polearm counter: cue, star 8, wide sweep 18 (disk r 4.5).
function rlk:boss/raiden/rig/play/counter_spear
function rlk:boss/raiden/fx/counter_cue
playsound minecraft:item.shield.block hostile @a[tag=player] ~ ~ ~ 1 1.4 0.2
function rlk:boss/raiden/hazard/new {k:1,a:4500,b:0,c:0,d:0,e:23040000,f:0,tol:300,tell:18,dmg:12,life:29,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
