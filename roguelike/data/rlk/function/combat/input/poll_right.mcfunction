# @s = 우클릭을 기록한 interaction. 실제 클릭 주인을 기록한 다음 원자적으로 소비한다.
execute unless data entity @s interaction run return 0
tag @a[tag=rlk_rc_owner] remove rlk_rc_owner
execute on target if entity @s[type=minecraft:player,tag=player] run tag @s add rlk_rc_owner
execute unless entity @a[tag=rlk_rc_owner,limit=1] run tag @a[tag=player,limit=1] add rlk_rc_owner
data remove entity @s interaction
execute as @a[tag=rlk_rc_owner] at @s run function rlk:combat/rclick_do
tag @a[tag=rlk_rc_owner] remove rlk_rc_owner
