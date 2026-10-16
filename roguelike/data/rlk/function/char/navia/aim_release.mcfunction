# 조준을 뗌 (@s = 플레이어, at 몸): 조준 끝 → 발사 모션 "skill_fire"(3틱에 발사) → 충전 소모
# 순서: 모션을 먼저 시작한다(조준 모션의 취소 처리가 새 발사 대기를 보지 않게)
function rlk:char/navia/aim_end
function rlk:char/motion/start {char:"navia",clip:"skill_fire"}
function rlk:char/navia/spend
execute unless score @s pmVisible matches 1 unless entity @e[tag=rlk_nvgun,limit=1] run function rlk:char/navia/gun_spawn
execute unless score @s pmVisible matches 1 run scoreboard players set @s nvGun 30
