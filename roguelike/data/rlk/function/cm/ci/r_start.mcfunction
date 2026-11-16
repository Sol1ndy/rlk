# picked by its caster (or its own timer when summoned alone for a test)
scoreboard players set @s cmS 1
scoreboard players set @s cmT 10
tag @s add rlk_c2_busy
scoreboard players set @s cmCd 50
particle minecraft:electric_spark ~ ~0.5 ~ 0.2 0.2 0.2 0.05 8
playsound minecraft:entity.vex.charge master @a ~ ~ ~ 0.9 1.4
