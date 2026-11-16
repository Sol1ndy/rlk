# 발사 틱 전에 스킬 모션이 끊김 (@s = 플레이어, motion/control/cancel 에서): 이미 소모한 충전의 발사를 지금 낸다
# 사망 · 선택 공간 · 다른 캐릭터로 바뀐 경우에는 버린다
scoreboard players set #nvFire tmp 1
execute if score @s dead matches 1 run scoreboard players set #nvFire tmp 0
execute if score @s pkMode matches 1.. run scoreboard players set #nvFire tmp 0
execute unless score #charN tmp matches 6 run scoreboard players set #nvFire tmp 0
execute unless entity @e[tag=rlk_body,limit=1] run scoreboard players set #nvFire tmp 0
# 방향은 char/navia/fire_dir 가 정한다(방향 고정 클립은 몸이 바라보는 기준 방향, 아니면 시선)
execute if score #nvFire tmp matches 1 run function rlk:char/navia/fire_dir
scoreboard players set @s nvShot 0
