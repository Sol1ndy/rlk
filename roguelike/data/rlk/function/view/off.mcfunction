# 숄더뷰 시점 끄기(원래의 1인칭). 사용: /function rlk:view/off
scoreboard players set #on view 0
function rlk:view/rays
tellraw @s [{"text":"[시점] ","color":"gold","bold":true},{"text":"숄더뷰를 껐습니다. 켜기: ","color":"gray","bold":false},{"text":"/function rlk:view/on","color":"yellow","bold":false,"click_event":{"action":"suggest_command","command":"/function rlk:view/on"}}]
