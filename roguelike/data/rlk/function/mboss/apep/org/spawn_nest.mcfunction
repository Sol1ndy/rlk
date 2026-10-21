# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# A 둥지 (nest, apK 4) at the execution position: HP 26 per mille of #apTot, RES Dendro 20 / others 10.
scoreboard players operation #auxHp mb = #apTot mb
scoreboard players set #apX mb 26
scoreboard players operation #auxHp mb *= #apX mb
scoreboard players operation #auxHp mb /= #c1000 mb
execute if score #auxHp mb matches ..0 run scoreboard players set #auxHp mb 1
scoreboard players set #auxRes mb 10
scoreboard players set #auxResEl mb 7
scoreboard players set #auxResElV mb 20
scoreboard players set #auxShW mb 16
scoreboard players set #auxShH mb 22
function rlk:mboss/aux/spawn
execute as @e[type=minecraft:husk,tag=rlk_mb_auxlast,limit=1] at @s run function rlk:mboss/apep/org/init_nest
