# @s = the boss: the palms flash (14 t star) and the clap zone locks between them.
execute at @e[tag=rlk_rd_tm_hl,limit=1] run function rlk:boss/raiden/fx/clap_star
execute at @e[tag=rlk_rd_tm_hr,limit=1] run function rlk:boss/raiden/fx/clap_star
execute at @e[tag=rlk_rd_tm_clapc,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:3000,b:0,c:0,d:0,e:10890000,f:0,tol:300,tell:14,dmg:16,life:25,ev:10,max:1,grp:0,dk:0,dl:0,kb:0,sv:1,snd:1,nd:0,jp:0,det:0,lf:0,fv:0}
