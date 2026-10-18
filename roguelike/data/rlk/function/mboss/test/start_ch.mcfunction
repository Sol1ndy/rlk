# /function rlk:mboss/test/start_ch {id:"proto",ch:2}
execute unless entity @s[tag=player] run return run tellraw @s {text:"[중간보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},{text:"/function rlk:room/setup",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:room/setup'}},{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #mbTest mb matches 1 run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},{text:"/function rlk:run/stop",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:run/stop'}},{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 중간보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
$execute unless data storage rlk:mboss byid.$(id) run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"등록되지 않았거나 꺼진 중간보스입니다: $(id)",color:"gray",bold:false}]
$execute store result score #mbForce mb run data get storage rlk:mboss byid.$(id).n
# the boss of this test, for the replay links (test/defeat runs after test/end has forgotten cur)
$data modify storage rlk:mboss tlast set value {id:"$(id)"}
$scoreboard players set #mbReqCh mb $(ch)
execute unless score #mbReqCh mb matches 1.. run scoreboard players set #mbReqCh mb 1
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #mbTest mb 1
scoreboard players set #mbLock mb 0
scoreboard players set #active room 1
scoreboard players operation #chapter room = #mbReqCh mb
scoreboard players set #mapIdx room 2
scoreboard players set #mapType room 1
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
data modify storage rlk:room next set value [15]
data modify storage rlk:mboss met set value []
execute in minecraft:overworld run function rlk:room/gen
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=15,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld at @e[tag=rlk_zone,scores={zkind=15},limit=1] run tp @s ~ ~ ~ 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=15,zst=1}] at @s run function rlk:room/zone_enter
execute in minecraft:overworld as @e[tag=rlk_obj,scores={oact=14},limit=1] at @s run function rlk:mboss/gate
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"중간보스 시험 전투를 시작합니다. 1.5초 뒤 경기장으로 이동합니다.",color:"gray",bold:false}]
function rlk:mboss/test/help
