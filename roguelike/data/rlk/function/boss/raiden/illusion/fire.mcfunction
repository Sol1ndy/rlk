# As a clone at its feet, its yaw: every clone cuts the diagonal (\ wave); the real one also cuts back 4 t later
# (/ wave): the X.
function rlk:boss/raiden/hazard/new {k:6,a:500,b:800000,c:2600,d:1000,e:5000,f:30,tol:300,tell:1,dmg:10,life:32,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:3,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
execute if score @s rdReal matches 1 run function rlk:boss/raiden/hazard/new {k:6,a:500,b:800000,c:2600,d:1000,e:5000,f:30,tol:300,tell:5,dmg:10,life:36,ev:10,max:1,grp:1,dk:0,dl:0,kb:0,sv:2,sm:0,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
tag @e[tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz
