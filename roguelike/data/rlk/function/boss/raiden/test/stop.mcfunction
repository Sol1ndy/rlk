# /function rlk:boss/raiden/test/stop: remove the fight (bars included) and return to the lobby.
execute unless score #rdTest rd matches 1 run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"진행 중인 보스 테스트가 없습니다.",color:"gray",bold:false}]
function rlk:boss/raiden/test/end
tellraw @a[tag=player] [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"보스 테스트를 끝내고 로비로 돌아왔습니다.",color:"gray",bold:false}]
