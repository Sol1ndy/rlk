# /function rlk:mboss/test/special_ch {id:"tachy",ch:2} (= rlk:boss/test/special_ch): a run-less real fight (as
# test/chapter_ch): a real node map of chapter ch (#mapIdx 2, no nodes), the first combat room next to the start zone built
# with the forced rift of that special (#riftForce + spforce) and visited without mobs (room/zone_first: the rift opens at
# once), the player before it; test/swait enters it as soon as no arena job runs (#spAuto 1). {id:"help",ch:1}: the ids.
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_special_ch
execute unless entity @s[tag=player] run return run tellraw @s {text:"[특수 보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},{text:"/function rlk:room/setup",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:room/setup'}},{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #mbTest mb matches 1 run return run tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},{text:"/function rlk:run/stop",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:run/stop'}},{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 특수 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
$execute unless data storage rlk:mboss sbyid.$(id) run return run tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"등록되지 않았거나 꺼진 특수 보스입니다: $(id)",color:"gray",bold:false}]
$data modify storage rlk:mboss tlast set value {id:"$(id)",ch:1,sp:1b}
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
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
scoreboard players set #active room 1
scoreboard players operation #chapter room = #mbReqCh mb
scoreboard players set #mapIdx room 2
scoreboard players set #mapType room 1
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
data modify storage rlk:room next set value []
data modify storage rlk:mboss spmet set value []
execute in minecraft:overworld run function rlk:room/gen
$data modify storage rlk:mboss spforce set value {id:"$(id)"}
scoreboard players set #riftForce room 1
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rlk_zone,scores={zid=1},limit=1] at @s as @e[type=minecraft:marker,tag=rlk_zone,scores={zkind=1,zst=0},sort=nearest,limit=1] run function rlk:room/zone_build
scoreboard players set #riftForce room 0
data remove storage rlk:mboss spforce
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rlk_zone,tag=rlk_riftz,scores={zst=1},limit=1] at @s run function rlk:room/zone_first
# zone_first queues the show of a visited zone for the next rift tick: show it now (the player is placed before it)
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rlk_zone,tag=rlk_riftq] at @s run function rlk:room/rift/show_now
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rlk_rift,limit=1] at @s rotated as @s rotated ~ 0 run function rlk:mboss/test/sstand
function rlk:view/sync
scoreboard players operation @s curHealth = @s maxHealth
execute unless entity @e[type=minecraft:marker,tag=rlk_rift,limit=1] run return run tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"균열을 놓을 전투 구역을 찾지 못했습니다. 다시 실행하세요.",color:"gray",bold:false}]
tellraw @s [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"특수 보스 시험 전투를 시작합니다. 경기장이 준비되면 균열에 자동으로 들어갑니다.",color:"gray",bold:false}]
function rlk:mboss/test/shelp
scoreboard players set #spAuto mb 1
scoreboard players set #spWaitT mb 0
schedule function rlk:mboss/test/swait 5t replace
