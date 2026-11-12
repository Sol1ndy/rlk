# 결정 축포 바로 발사 (@s = 플레이어, at 몸): 스킬 모션 "skill"(7틱에 발사, 그때까지 행동 잠금) → 충전 소모
# 순서: 모션을 먼저 시작한다(이전 모션의 취소 처리가 새 발사 대기를 보지 않게)
function rlk:char/motion/start {char:"navia",clip:"skill"}
function rlk:char/navia/spend
# 1인칭(몸 디스플레이 없음)에서만 블록 우산총을 보인다. 숄더뷰에서는 모션의 우산 모델이 대신한다
execute unless score @s pmVisible matches 1 run function rlk:char/navia/gun_spawn
execute unless score @s pmVisible matches 1 run scoreboard players set @s nvGun 30
