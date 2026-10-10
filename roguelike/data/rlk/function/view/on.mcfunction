# 숄더뷰 시점 켜기. 사용: /function rlk:view/on
scoreboard players set #on view 1
scoreboard players set #vmode view 2
execute as @a[tag=player] run function rlk:view/ride_off
function rlk:view/rays
tellraw @s [{"text":"[시점] ","color":"gold","bold":true},{"text":"숄더뷰(3인칭)를 켰습니다. 끄기: ","color":"gray","bold":false},{"text":"/function rlk:view/off","color":"yellow","bold":false,"click_event":{"action":"suggest_command","command":"/function rlk:view/off"}}]
