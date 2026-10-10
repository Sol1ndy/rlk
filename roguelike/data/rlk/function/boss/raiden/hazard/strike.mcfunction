scoreboard players operation #rdVfxOwner rd = @s rdHId
execute as @e[type=minecraft:item_display,tag=rlk_rd_hvfx] if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_strike
playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.50 1.25 0.2
execute if score @s rdShape matches 4..8 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.60 1.35 0.25
execute if score @s rdShape matches 12 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.55 1.5 0.25
function rlk:boss/raiden/hazard/hit
