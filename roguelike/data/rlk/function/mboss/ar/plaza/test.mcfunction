# Rebuild the plaza and look at it (outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"런 중에는 쓸 수 없습니다.",color:"gray",bold:false}]
execute in minecraft:overworld run function rlk:mboss/arena/rebuild
execute in minecraft:overworld run tp @s 200.5 201 8.5 180 0
function rlk:view/sync
tellraw @s [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"경기장을 다시 지었습니다. 돌아가기: ",color:"gray",bold:false},{text:"/function rlk:lobby/go",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:lobby/go'}}]
