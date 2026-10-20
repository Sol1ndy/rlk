# slide #azPT 137
data modify storage rlk:mboss az.tl set value {id:2,r0:40,r1:180,w:35,tell:1,dur:5,nd:0,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/fx/tele/wave with storage rlk:mboss az.tl
execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/front/1 {r0:400,r1:1800,w:350,dur:5}
execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/front/2 {r0:400,r1:1800,w:350,dur:5}
execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/front/3 {r0:400,r1:1800,w:350,dur:5}
execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/front/4 {r0:400,r1:1800,w:350,dur:5}
execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/front/5 {r0:400,r1:1800,w:350,dur:5}
