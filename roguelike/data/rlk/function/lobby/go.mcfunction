# 로비로 (@s = 플레이어): 지금 있던 방을 정리하고 로비 시작 자리로. 부활 지점도 로비
function rlk:lobby/leave
function rlk:lobby/tp {x:"93.5",y:"193",z:"32.5",yaw:"180"}
spawnpoint @s 93 193 32 180 0
scoreboard players set @s lobRoom 1
title @s actionbar {text:"로비",color:"#FFD24A"}
scoreboard players set @s hudHold 30
