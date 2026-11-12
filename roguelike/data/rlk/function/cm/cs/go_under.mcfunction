# under the sand: no rlk_mob (player attacks / AoE / auto-aim skip it, no health bar), rlk_pet (mob/setup leaves
# it alone), Invulnerable (a stray vanilla hit does nothing). Still rlk_zmob: the room waits for it, it surfaces on a timer.
tag @s add rlk_c3_under
tag @s add rlk_pet
tag @s remove rlk_mob
data merge entity @s {Invulnerable:1b}
tag @s remove rlk_cmch
scoreboard players set @s cmS 2
scoreboard players set @s cmT 50
scoreboard players set @s cmN 0
playsound minecraft:block.sand.break master @a ~ ~ ~ 1 0.6
