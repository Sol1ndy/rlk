# As the boss at the arena centre; each illusion faces its own running direction.
function rlk:boss/raiden/illusion/spawn {id:1}
execute rotated ~90 0 run function rlk:boss/raiden/illusion/spawn {id:2}
execute rotated ~180 0 run function rlk:boss/raiden/illusion/spawn {id:3}
execute rotated ~270 0 run function rlk:boss/raiden/illusion/spawn {id:4}
# One random illusion is the real body; every illusion gets one turn, random order.
execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1
execute as @e[tag=rlk_rd_illusion,scores={rdTurns=0},sort=random,limit=1] run scoreboard players set @s rdTurns 1
execute as @e[tag=rlk_rd_illusion,scores={rdTurns=0},sort=random,limit=1] run scoreboard players set @s rdTurns 2
execute as @e[tag=rlk_rd_illusion,scores={rdTurns=0},sort=random,limit=1] run scoreboard players set @s rdTurns 3
execute as @e[tag=rlk_rd_illusion,scores={rdTurns=0},sort=random,limit=1] run scoreboard players set @s rdTurns 4
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~1 ~ 1 1.15 0.2
playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~1 ~ 0.7 1.4 0.2
