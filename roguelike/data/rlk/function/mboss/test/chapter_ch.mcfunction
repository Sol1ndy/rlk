# /function rlk:mboss/test/chapter_ch {id:"cproto",ch:2}: a real boss map (#mapIdx 5, #mapType 8) of that chapter routed
# to the chapter boss (#cbForce, only under #mbTest 1): room/gen -> cb/route_force -> the entrance layout, the kind-9 zone
# built (-> cb/prep: cprep, forceload, the sliced arena job), the player in front of the gate (zone_enter -> k_cboss);
# test/cwait presses the gate as soon as no arena job runs (#cbAuto 1).
execute unless entity @s[tag=player] run return run tellraw @s {text:"[챕터 보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},{text:"/function rlk:room/setup",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:room/setup'}},{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #mbTest mb matches 1 run return run tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},{text:"/function rlk:run/stop",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:run/stop'}},{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
$execute unless data storage rlk:mboss cbyid.$(id) run return run tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"등록되지 않았거나 꺼진 챕터 보스입니다: $(id)",color:"gray",bold:false}]
$execute store result score #mbReqF mb run data get storage rlk:mboss cbyid.$(id).n
$data modify storage rlk:mboss tlast set value {id:"$(id)",ch:1,cb:1b}
$scoreboard players set #mbReqCh mb $(ch)
execute unless score #mbReqCh mb matches 1.. run scoreboard players set #mbReqCh mb 1
execute store result storage rlk:mboss tlast.ch int 1 run scoreboard players get #mbReqCh mb
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #mbTest mb 1
scoreboard players set #mbLock mb 0
scoreboard players set #mbForce mb 0
scoreboard players operation #cbForce mb = #mbReqF mb
scoreboard players set #cbAuto mb 1
scoreboard players set #active room 1
scoreboard players operation #chapter room = #mbReqCh mb
scoreboard players set #mapIdx room 5
scoreboard players set #mapType room 8
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
execute in minecraft:overworld run function rlk:room/gen
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=9,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld at @e[tag=rlk_zone,scores={zkind=9},limit=1] positioned ~ ~ ~4 run tp @s ~ ~ ~ 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=9,zst=1}] at @s run function rlk:room/zone_enter
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"챕터 보스 시험 전투를 시작합니다. 경기장이 준비되면 문을 자동으로 누릅니다.",color:"gray",bold:false}]
function rlk:mboss/test/chelp
scoreboard players set #cbWaitT mb 0
schedule function rlk:mboss/test/cwait 5t replace
