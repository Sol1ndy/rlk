execute positioned ~ ~0.5 ~ run function rlk:boss/raiden/rig/prop/blade_eye
tag @e[tag=rlk_rd_prop_new] add rlk_rd_sgfx
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
function rlk:boss/raiden/hazard/new {k:1,a:2000,b:0,c:0,d:0,e:5290000,f:0,tol:300,tell:12,dmg:8,life:23,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,sm:0,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
tag @e[tag=rlk_rd_hazard,scores={rdHAge=-1},distance=..0.01] add rlk_rd_nobal
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.9 1.6 0.2
