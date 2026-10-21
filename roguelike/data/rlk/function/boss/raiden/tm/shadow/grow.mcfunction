# @s = the boss, tick 69: the pool stops; the slam (disk r 4.5, lift) locks where it stopped and its pool decal
# grows from the pool size in 4 t.
kill @e[tag=rlk_rd_tm_spot]
execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_spot"]}
execute unless entity @e[tag=rlk_rd_tm_spot] at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_spot"]}
execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/hazard/new {k:1,a:4500,b:0,c:0,d:0,e:23040000,f:0,tol:300,tell:15,dmg:24,life:26,ev:10,max:1,grp:0,dk:6,dl:0,kb:5,sv:1,sm:0,snd:1,nd:0,jp:0,det:0,lf:1,fv:0}
data modify entity @e[tag=rlk_rd_decal_pool,tag=rlk_rd_fxnew,limit=1] transformation.scale set value [1.5f,1f,1.5f]
data modify entity @e[tag=rlk_rd_decal_pool,tag=rlk_rd_fxnew,limit=1] item.components."minecraft:custom_data".d set value 4
