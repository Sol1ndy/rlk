# up to the cap of 4, from just above its head (a cell the brain itself stands in).
# cm/init (run by each new cicin) overwrites #cid: keep the caster id in #c2cc and restore #cid after
scoreboard players operation #c2lv tmp = @s mlv
scoreboard players operation #c2cc tmp = @s cmId
scoreboard players set #c2k tmp 4
scoreboard players operation #c2k tmp -= #ccN tmp
execute if score #c2k tmp matches 1.. positioned ~ ~1.5 ~ run function rlk:cm/cc/summon_one {a:0}
execute if score #c2k tmp matches 2.. positioned ~ ~1.5 ~ run function rlk:cm/cc/summon_one {a:90}
execute if score #c2k tmp matches 3.. positioned ~ ~1.5 ~ run function rlk:cm/cc/summon_one {a:180}
execute if score #c2k tmp matches 4.. positioned ~ ~1.5 ~ run function rlk:cm/cc/summon_one {a:270}
scoreboard players operation #cid tmp = @s cmId
scoreboard players set @s c2eF 1
scoreboard players set @s cmD 30
scoreboard players set @s cmS 2
scoreboard players set @s cmT 8
particle minecraft:electric_spark ~ ~2 ~ 0.5 0.4 0.5 0.1 20
playsound minecraft:entity.evoker.cast_spell master @a ~ ~ ~ 1 1.4
