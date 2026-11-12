# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# A 기본 (basic, apK 1) at the execution point (any executor; tests 23-28, the pending spawn
# markers): HP 17 per mille of #apTot, RES Dendro 20 / others 10 (U2), the click shield
# 1.2 x 1.6 and the HP bar 1.6 b above the feet (FN-29), the models (om/basic/spawn).
scoreboard players operation #auxHp mb = #apTot mb
scoreboard players set #apX mb 17
scoreboard players operation #auxHp mb *= #apX mb
scoreboard players operation #auxHp mb /= #c1000 mb
execute if score #auxHp mb matches ..0 run scoreboard players set #auxHp mb 1
scoreboard players set #auxRes mb 10
scoreboard players set #auxResEl mb 7
scoreboard players set #auxResElV mb 20
scoreboard players set #auxShW mb 12
scoreboard players set #auxShH mb 16
scoreboard players set #auxHbY mb -6
execute positioned ~ 201 ~ run function rlk:mboss/aux/spawn
execute as @e[type=minecraft:husk,tag=rlk_mb_auxlast,limit=1] at @s run function rlk:boss/apep/org/init_basic
