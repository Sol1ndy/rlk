# @s = the shard: a shield of 12 % max HP for 15 s with the brand element (own copy of the
# crystallize pickup, not counted against the crystal cap); the element only when the new amount >= the shield.
execute store result score #amt tmp run scoreboard players get @a[tag=player,limit=1] maxHealth
scoreboard players set #azX mb 120
scoreboard players operation #amt tmp *= #azX mb
scoreboard players operation #amt tmp /= #c1000 mb
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
scoreboard players operation #shEl tmp = @s azS
execute as @a[tag=player,limit=1] unless score @s shieldHP > #amt tmp run function rlk:element/shield_gain
scoreboard players set #shEl tmp 0
function rlk:boss/azhdaha/fx/snd/shard_pick
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.2 0.33
kill @s
