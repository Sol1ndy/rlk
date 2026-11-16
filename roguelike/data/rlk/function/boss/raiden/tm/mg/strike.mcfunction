# @s = the boss, tick 151: the slash (hit 152) as a safe dome: inside the raised dome 1 damage, anywhere else fatal;
# without a dome the safe radius is nil. The katana comes down on a raised dome: the scar of light along its rake.
execute at @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/hazard/new {k:10,a:8000,b:0,c:0,d:0,e:64000000,f:0,tol:300,tell:1,dmg:1,life:12,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:0,sm:0,go:0,sp:0,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute unless entity @e[tag=rlk_rd_dome,limit=1] at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/hazard/new {k:10,a:1,b:0,c:0,d:0,e:1,f:0,tol:300,tell:1,dmg:1,life:12,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:0,sm:0,go:0,sp:0,snd:1,nd:1,jp:0,det:0,lf:0,fv:0}
execute if entity @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/judgment_rig/scar
