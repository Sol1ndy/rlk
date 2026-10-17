# Per-fight constants from rlk:mboss cur (read by hurt, gold_drop, the shells and the libraries).
scoreboard players set #mbKilled mb 0
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute store result score #mbId mb run data get storage rlk:mboss cur.n
execute store result score #mbDmgMul mb run data get storage rlk:mboss cur.dmgMul
execute store result score #mbGoldMul mb run data get storage rlk:mboss cur.goldMul
execute store result score #mbSap mb run data get storage rlk:mboss cur.sap
execute store result score #mbIntro mb run data get storage rlk:mboss cur.intro
execute store result score #mbDeath mb run data get storage rlk:mboss cur.death
execute store result score #mbEl mb run data get storage rlk:mboss cur.el
execute store result score #mbAtk mb run data get storage rlk:mboss cur.atk
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
data modify storage rlk:mboss aura set value []
scoreboard players set #mbAuraK mb -1
function rlk:mboss/opts_reset
