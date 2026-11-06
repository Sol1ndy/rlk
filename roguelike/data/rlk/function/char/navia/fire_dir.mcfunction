# 결정 축포 발사 방향 정하기 (@s = 플레이어; events/navia/skill 7틱 · skill_fire 3틱 · shot_cancel 에서) → char/navia/fire
# 탄은 몸(rlk_body: 숄더뷰는 아바타, 1인칭은 플레이어)의 눈 높이에서 몸이 보는 방향으로 나간다. 숄더뷰의 아바타는 스킬을 누른 순간부터
# 조준점을 본다(view/face_lock · 조준 중 nvA · 뗄 때 aim_release 의 face_lock). 그래서 탄이 카메라 시선과 나란히 옆으로 비껴가지 않고
# 조준선이 가리킨 곳으로 모인다(카메라는 몸에서 좌우 0.9칸 떨어져 있다).
# 방향이 고정된 클립(바로 발사 "skill", basis "body": 시작 방향 = 누른 순간 아바타가 조준점을 본 방향)은 좌우를 그 기준 방향으로,
# 높낮이는 지금 몸이 보는 높낮이로 쏜다. 그래서 카메라를 돌려도 탄·피해·총구 효과가 우산을 든 몸과 어긋나지 않는다.
execute unless score @s pmVisible matches 1 at @e[tag=rlk_body,limit=1] run return run function rlk:char/navia/fire
execute unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] run return run function rlk:char/navia/fire
execute unless entity @e[tag=rlk_pm_basis,limit=1] at @e[tag=rlk_body,limit=1] run return run function rlk:char/navia/fire
# 기준 방향(좌우) + 몸의 높낮이를 가진 임시 마커
kill @e[tag=rlk_nvaim]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nvaim"]}
data modify entity @e[tag=rlk_nvaim,limit=1] Rotation set from entity @e[tag=rlk_body,limit=1] Rotation
data modify entity @e[tag=rlk_nvaim,limit=1] Rotation[0] set from entity @e[tag=rlk_pm_basis,limit=1] Rotation[0]
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_nvaim,limit=1] run function rlk:char/navia/fire
kill @e[tag=rlk_nvaim]
