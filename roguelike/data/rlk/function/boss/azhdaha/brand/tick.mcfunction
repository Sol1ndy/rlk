# @s = body, at it, every module tick (after the clocks): the hit / dodge events of the framework (cm.md 13.3), the
# heal meter, the DoT clock, the rune, the shards. The events are read and cleared here.
execute if score #mbHitEv mb matches 1.. run function rlk:boss/azhdaha/brand/hit
scoreboard players set #mbHitEv mb 0
execute if score #mbDodgeEv mb matches 1.. run function rlk:boss/azhdaha/brand/dodge
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
execute as @a[tag=player,scores={azBrT=1..},limit=1] run function rlk:boss/azhdaha/brand/heal
execute unless entity @a[tag=player,scores={azBrT=1..},limit=1] run scoreboard players set #mbHealAmt mb 0
execute as @a[tag=player,scores={azBrT=1..},limit=1] run function rlk:boss/azhdaha/brand/clock
execute as @a[tag=player,scores={azBrT=1..},limit=1] run function rlk:boss/azhdaha/brand/rune_t
execute if entity @e[type=minecraft:item_display,tag=rlk_az_shard,limit=1] run function rlk:boss/azhdaha/brand/shard_tick
scoreboard players set #azBrCs mb 0
