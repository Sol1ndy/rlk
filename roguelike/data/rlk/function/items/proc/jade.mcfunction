scoreboard players operation #amt tmp = @s maxHealth
scoreboard players operation #amt tmp *= #jadePct tmp
scoreboard players operation #amt tmp /= #100 tmp
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
function rlk:element/shield_gain
scoreboard players operation @s shieldT = #jadeDur tmp
scoreboard players operation #jadeT itv = #jadeDur tmp
playsound minecraft:block.anvil.land master @a ~ ~ ~ 0.25 0.7
