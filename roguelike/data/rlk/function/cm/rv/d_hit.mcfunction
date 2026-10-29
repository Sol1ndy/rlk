scoreboard players set #cmDmg tmp 18
scoreboard players set #cmEl tmp 1
scoreboard players operation #cmLv tmp = @s mlv
function rlk:cm/hit_pl
scoreboard players set @s c2eF 1
execute at @s run particle minecraft:flame ~ ~0.8 ~ 0.4 0.4 0.4 0.08 16
execute at @s run playsound minecraft:entity.blaze.hurt master @a ~ ~ ~ 0.8 0.8
