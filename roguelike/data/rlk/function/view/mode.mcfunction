# 시점 종류 바꾸기: /function rlk:view/mode {m:1} (1 숄더뷰 · 2 F5 위쪽 시점). 켜져 있지 않으면 켠다
$scoreboard players set #vmode view $(m)
execute as @a[tag=player] run function rlk:view/ride_off
execute as @a[tag=player] run ride @s dismount
scoreboard players set #on view 1
function rlk:view/rays
