# After mboss/repool (#mbRamp 30..1): the new pool's bar refills over 30 t (#buHp x (30 - ramp) / 30, overflow-safe).
scoreboard players remove #mbRamp mb 1
scoreboard players set #t mb 30
scoreboard players operation #t mb -= #mbRamp mb
scoreboard players operation #h mb = #buHp bu
execute if score #h mb matches 10000000.. run scoreboard players operation #buHp bu /= #c30 mb
scoreboard players operation #buHp bu *= #t mb
execute if score #h mb matches ..9999999 run scoreboard players operation #buHp bu /= #c30 mb
