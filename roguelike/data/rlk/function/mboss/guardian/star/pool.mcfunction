# #auxHp = body max HP x #gdPm / 1000 (overflow-safe); #auxHpPct stays 0 so aux/spawn uses #auxHp.
scoreboard players operation #gdX mb = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] mhpM
execute if score #gdX mb matches 2000000.. run scoreboard players operation #gdX mb /= #c1000 mb
execute if score #gdX mb matches 2000000.. run scoreboard players operation #gdX mb *= #gdPm mb
execute if score #gdX mb matches ..1999999 run scoreboard players operation #gdX mb *= #gdPm mb
execute if score #gdX mb matches ..1999999 run scoreboard players operation #gdX mb /= #c1000 mb
execute if score #gdX mb matches ..0 run scoreboard players set #gdX mb 1
scoreboard players operation #auxHp mb = #gdX mb
scoreboard players set #auxHpPct mb 0
