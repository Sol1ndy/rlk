# Rebuild cp_test (a sliced job) and look at it from its arrival spot (outside a run; the job's done releases the
# forceload again, outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"런 중에는 쓸 수 없습니다.",color:"gray",bold:false}]
function rlk:mboss/ar/cp_test/fl_on
execute in minecraft:overworld run function rlk:mboss/arena/cp_test/rebuild
execute in minecraft:overworld run tp @s 540.5 201 17.5 180 0
function rlk:view/sync
tellraw @s [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"경기장 cp_test 을(를) 다시 짓는 중입니다(여러 틱; 다 지으면 강제 로드를 풉니다). 돌아가기: ",color:"gray",bold:false},{text:"/function rlk:lobby/go",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:lobby/go'}}]
