# 결정 축포 발사 방향 정하기 (@s = 플레이어; events/navia/skill 7틱 · skill_fire 3틱 · shot_cancel 에서) → char/navia/fire
# 숄더뷰에서 방향이 고정된 클립(바로 발사 "skill": 끝에 우산을 세워 두므로 시작 방향 고정)은 몸 디스플레이가 바라보는 기준 방향으로 쏜다.
# 높낮이는 지금 시선을 따른다(몸은 위아래로 기울지 않는다). 그래서 카메라를 돌려도 탄·피해·총구 효과가 몸 옆으로 나가지 않는다.
# 그 밖(조준 후 발사 "skill_fire"는 몸이 매 틱 시선 방향으로 돈다 · 1인칭은 블록 우산총이 시선을 따른다)은 플레이어 시선 그대로.
execute unless score @s pmVisible matches 1 at @e[tag=rlk_body,limit=1] rotated as @s run return run function rlk:char/navia/fire
execute unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @s run return run function rlk:char/navia/fire
execute unless entity @e[tag=rlk_pm_basis,limit=1] at @e[tag=rlk_body,limit=1] rotated as @s run return run function rlk:char/navia/fire
# 기준 방향(좌우) + 시선(높낮이)을 가진 임시 마커
kill @e[tag=rlk_nvaim]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nvaim"]}
data modify entity @e[tag=rlk_nvaim,limit=1] Rotation set from entity @s Rotation
data modify entity @e[tag=rlk_nvaim,limit=1] Rotation[0] set from entity @e[tag=rlk_pm_basis,limit=1] Rotation[0]
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_nvaim,limit=1] run function rlk:char/navia/fire
kill @e[tag=rlk_nvaim]
