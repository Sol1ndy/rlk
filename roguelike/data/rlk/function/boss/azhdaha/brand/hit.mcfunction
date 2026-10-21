# @s = body. A landed hit this tick (#mbHitEl element, #mbHitRA 1 lingering, #mbHitSh 1 shielded before it): brand
# only for an absorbed element (phase >= 2: the leg element; phase 3: the tail element too).
scoreboard players set #azX mb 0
execute if score #azPh mb matches 2..3 if score #mbHitEl mb = #azLeg mb run scoreboard players set #azX mb 1
execute if score #azPh mb matches 3 if score #mbHitEl mb = #azTail mb run scoreboard players set #azX mb 1
execute if score #azX mb matches 0 run return 0
scoreboard players operation #azBrIn mb = #mbHitEl mb
execute if score #mbHitRA mb matches 1.. run return run function rlk:boss/azhdaha/brand/linger
scoreboard players set #azBrStrike mb 1
execute as @a[tag=player,limit=1] run function rlk:boss/azhdaha/brand/apply
execute unless score #mbHitSh mb matches 1.. as @a[tag=player,limit=1] run function rlk:boss/azhdaha/brand/shard_try
