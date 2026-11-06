# view/mode 의 본문 (macro: m = 1 | 2). view/mode 가 {m:"help"} 를 먼저 거른 뒤 부른다
$scoreboard players set #vmode view $(m)
execute as @a[tag=player] run function rlk:view/ride_off
execute as @a[tag=player] run ride @s dismount
scoreboard players set #on view 1
function rlk:view/rays
