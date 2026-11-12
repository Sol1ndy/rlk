# 고른 카드에 미리 보여 준 아이템(rlk:room gid)을 준다 (@s = 플레이어). 보유 칸이 가득하면 나갈 때 발밑에(dropq)
execute unless data storage rlk:room gid run return 0
execute if data storage rlk:room {gid:""} run return 0
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp >= @s invCap run return run data modify storage rlk:lvpick dropq append from storage rlk:room gid
data modify storage rlk:room b.id set from storage rlk:room gid
function rlk:items/give with storage rlk:room b
