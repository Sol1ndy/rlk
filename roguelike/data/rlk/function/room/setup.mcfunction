# 던전 구역 준비 (@s = player 태그 플레이어). 사용: /function rlk:room/setup   ※ 월드당 한 번
# 오버월드 x -64~63, z -64~63, y 186~230 을 던전 전용으로 쓴다(이 범위의 블록은 지워짐!)
execute unless entity @s[tag=player] run return run tellraw @s {"text":"[방] 'player' 태그가 있는 플레이어로 실행하세요.","color":"red"}
execute if score #active room matches 1 run function rlk:run/stop
function rlk:room/remove_old
execute in minecraft:overworld run forceload add -64 -64 63 63
# 중간보스 원형 경기장 청크 고정(room/remove 가 풀었을 수 있음, /reload 없이도 다시 걸리게)
execute in minecraft:overworld run forceload add 176 -16 223 31
data modify storage rlk:room ready set value 0b
scoreboard players set #setup room 0
tag @a remove rlk_setup
tag @s add rlk_setup
tellraw @s [{"text":"[방] ","color":"gold","bold":true},{"text":"던전 구역을 준비하는 중…","color":"gray","bold":false}]
schedule function rlk:room/setup2 40t
