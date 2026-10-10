# 방 사이 이동 (@s = 플레이어). macro: x y z yaw
$tp @s $(x) $(y) $(z) $(yaw) 0
function rlk:view/sync
scoreboard players set @s uiCd 6
