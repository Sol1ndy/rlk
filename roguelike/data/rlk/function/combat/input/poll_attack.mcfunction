# @s = 클릭을 기록한 interaction. 클릭 처리 중 UI/몹/실드가 사라져도 입력을 먼저 소비한다.
execute unless data entity @s attack run return 0
# 오래된/불완전한 기록에 timestamp가 없으면 현재 틱으로 처리한다.
execute store result score #lcStamp tmp run time query gametime
execute if data entity @s attack.timestamp store result score #lcStamp tmp run data get entity @s attack.timestamp 1
tag @a[tag=rlk_lc_owner] remove rlk_lc_owner
execute on attacker if entity @s[type=minecraft:player,tag=player] run tag @s add rlk_lc_owner
# 1인 전용 맵: 관계가 소실된 기록도 활성 플레이어에게 돌려준다.
execute unless entity @a[tag=rlk_lc_owner,limit=1] run tag @a[tag=player,limit=1] add rlk_lc_owner
data remove entity @s attack
execute as @a[tag=rlk_lc_owner] at @s run function rlk:combat/input/attack
tag @a[tag=rlk_lc_owner] remove rlk_lc_owner
