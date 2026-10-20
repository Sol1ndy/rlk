# jump l at tick 31 (positioned / rotated at rlk_mb_az_p2l)
data modify storage rlk:mboss az.tl set value {id:1,r0:30,r1:105,w:25,tell:1,dur:5,nd:0,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/fx/tele/wave with storage rlk:mboss az.tl
execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/front/1 {r0:30,r1:105,w:25,dur:5}
execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/front/2 {r0:30,r1:105,w:25,dur:5}
execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/front/3 {r0:30,r1:105,w:25,dur:5}
execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/front/4 {r0:30,r1:105,w:25,dur:5}
execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/front/5 {r0:30,r1:105,w:25,dur:5}
