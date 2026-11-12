# 분열로 생긴 몹 (@s): 방 몹 준비 뒤 부모 레벨(#c2PLv)로 맞춤
function rlk:room/mob_init
execute if score #c2PLv tmp matches 1.. run scoreboard players operation @s mlv = #c2PLv tmp
function rlk:mob/level_apply
