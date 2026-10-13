# /function rlk:boss/raiden/test/start (@s = 'player'): fight only Narukami, normal phase.
# Uses the real boss room (room/raiden layout in the forceloaded dungeon area) and the
# run flags (#active room 1) so room tick, death and cleanup flows all behave as in a run.
# Re-running restarts the fight. Player death or test/stop returns to the lobby.
execute unless entity @s[tag=player] run return run tellraw @s {text:"[보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},{text:"/function rlk:room/setup",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:room/setup"}},{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #rdTest rd matches 1 run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},{text:"/function rlk:run/stop",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:run/stop"}},{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
# Peaceful discards the husk body at once, which would read as an instant win.
execute store result score #rdDiff rd run difficulty
execute if score #rdDiff rd matches 0 run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"난이도가 '평화로움'이면 나루카미가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
# The map screen restores its saved position/game mode on close: close it before moving.
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #rdTest rd 1
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
# Stage-2 boss slot (Narukami's planned stage): level = (chapter-1)*6 + mapIdx + 1 = 12
# (test/level changes it).
scoreboard players set #active room 1
scoreboard players set #chapter room 2
scoreboard players set #mapIdx room 5
scoreboard players set #mapType room 8
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
execute in minecraft:overworld run function rlk:room/gen
# Open the arena at once, put the player inside facing the centre, start the fight now.
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld run tp @s 0.5 201 14.5 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=1}] at @s run function rlk:room/zone_enter
scoreboard players set #spawnT room 0
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2}] at @s run function rlk:room/mob_wave
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"나루카미 단독 전투를 시작합니다.",color:"white",bold:false}]
tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"명령: ",color:"gray",bold:false},{text:"start",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/start"}},{text:" 처음부터 · ",color:"gray",bold:false},{text:"armored",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/armored"}},{text:" 갑주 단계 · ",color:"gray",bold:false},{text:"pattern {id:N}",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/pattern {id:11}"}},{text:" 다음 패턴(1~7, 11~18) · ",color:"gray",bold:false},{text:"lock {id:N}",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/lock {id:11}"}},{text:" 패턴 고정(0 해제) · ",color:"gray",bold:false},{text:"level {lv:N}",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/level {lv:12}"}},{text:" 보스 레벨 · ",color:"gray",bold:false},{text:"stop",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/stop"}},{text:" 종료 후 로비",color:"gray",bold:false}]
