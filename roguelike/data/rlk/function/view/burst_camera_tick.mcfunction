# 궁극기 이동 잠금이 만드는 강한 FOV 확대를 카메라 거리 +30%로 완화한다.
# 5틱에 걸쳐 들어가고 복귀한다. 실제 이동·점프 잠금은 그대로 유지한다.
execute unless score #bcStep view matches 0..5 run scoreboard players set #bcStep view 0
scoreboard players operation #bcPrev view = #bcStep view
scoreboard players set #bcWant view 0
execute if score @s buT matches 1.. run scoreboard players set #bcWant view 1
execute if score @s pmActive matches 1 if score @s pmMoveLock matches 1 if data storage rlk:player_motion {active:{char:"arle",clip:"burst"}} run scoreboard players set #bcWant view 1
execute if score @s pmActive matches 1 if score @s pmMoveLock matches 1 if data storage rlk:player_motion {active:{char:"skirk",clip:"burst_metsu"}} run scoreboard players set #bcWant view 1
execute if score @s pmActive matches 1 if score @s pmMoveLock matches 1 if data storage rlk:player_motion {active:{char:"skirk",clip:"burst_jin"}} run scoreboard players set #bcWant view 1
execute if score @s pmActive matches 1 if score @s pmMoveLock matches 1 if data storage rlk:player_motion {active:{char:"navia",clip:"burst"}} run scoreboard players set #bcWant view 1
# 시점 해제·지도·사망·아이템 선택·개발자 모드는 원래 거리로 복귀한다.
execute unless score #on view matches 1 run scoreboard players set #bcWant view 0
execute if score @s devMode matches 1 run scoreboard players set #bcWant view 0
execute if score @s vMap matches 1 run scoreboard players set #bcWant view 0
execute if score @s dead matches 1 run scoreboard players set #bcWant view 0
execute if score @s pkMode matches 1.. run scoreboard players set #bcWant view 0
execute if score #bcWant view matches 1 if score #bcStep view matches ..4 run scoreboard players add #bcStep view 1
execute if score #bcWant view matches 0 if score #bcStep view matches 1.. run scoreboard players remove #bcStep view 1
execute unless score #bcStep view = #bcPrev view run function rlk:view/burst_camera_apply
