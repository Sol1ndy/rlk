# 게임 시작 (@s = 플레이어)
function rlk:lobby/leave
function rlk:run/start
# 시작하지 못했으면(던전 준비 전 등) 로비에 그대로
execute unless score #active room matches 1 run scoreboard players set @s lobRoom 1
