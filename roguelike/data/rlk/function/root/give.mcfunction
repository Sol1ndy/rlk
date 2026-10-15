# macro: mir = 각인 id. 그 각인이 달린 아이템(rlk:engravings byeng.<id>) 중 무작위 하나를 준다. 보유 칸이 가득하면 나갈 때 발밑에(dropq)
data remove storage rlk:room gid
$data modify storage rlk:room gq set from storage rlk:engravings byeng.$(mir)
execute store result score #gl tmp run data get storage rlk:room gq
execute if score #gl tmp matches ..0 run return 0
execute store result score #r tmp run random value 0..9999
scoreboard players operation #r tmp %= #gl tmp
execute store result storage rlk:room a.r int 1 run scoreboard players get #r tmp
function rlk:root/give2 with storage rlk:room a
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp >= @s invCap run return run data modify storage rlk:lvpick dropq append from storage rlk:room gid
data modify storage rlk:room b.id set from storage rlk:room gid
function rlk:items/give with storage rlk:room b
