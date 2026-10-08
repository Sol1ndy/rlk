# 조준점 (@s = 플레이어): 화면 가운데(조준선)가 가리키는 곳을 찾아 표식(rlk_aim)을 옮긴다
# 아바타는 평소엔 걷는 방향을 보고(view/move), 공격·스킬 직후나 조준 중일 때만 이 조준점을 본다 → 공격·스킬은 "아바타 눈에서 아바타가 보는 방향"으로 나가 조준선이 가리킨 곳에 맞는다
scoreboard players set #ai view 0
execute at @s anchored eyes positioned ^ ^ ^4 anchored feet run function rlk:view/aim_step
execute if score @s vAimT matches 1.. run scoreboard players remove @s vAimT 1
execute if score #lk view matches 1 run function rlk:view/face_aim
