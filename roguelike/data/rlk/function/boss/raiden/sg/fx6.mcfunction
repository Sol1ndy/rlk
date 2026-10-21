# 6 field lightning (A-02, sword after-effect): the pale disc under the player (locked), the bolt 20 t later.
scoreboard players set @s rdSgFxT 0
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/new {k:1,a:2500,b:0,c:0,d:0,e:7840000,f:0,tol:300,tell:20,dmg:8,life:31,ev:10,max:1,grp:0,dk:4,dl:0,kb:0,sv:2,snd:1,nd:0,jp:0,det:1,lf:0,fv:0}
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.7 0.2
