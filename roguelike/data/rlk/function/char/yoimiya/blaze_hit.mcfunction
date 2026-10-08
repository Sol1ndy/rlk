# 염초 정화의 춤으로 바뀐 화살이 맞음 (@s = 플레이어, 위치 = 맞은 곳)
# 원소 입자: 2초마다 1개, 스킬 한 번에 최대 4번
execute if score @s yoiPcCd matches ..0 if score @s yoiPcN matches ..3 run function rlk:char/yoimiya/blaze_pc
# 고유 특성 소매불 백경도: 스킬 지속 중 명중할 때마다 1스택(#yoiPDur 틱 유지, 최대 #yoiPMax)
execute unless score @s yoiSk matches 1.. run return 0
execute if score @s yoiP < #yoiPMax tmp run scoreboard players add @s yoiP 1
scoreboard players operation @s yoiPT = #yoiPDur tmp
