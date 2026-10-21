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
# chapter mode (AZ-CM): #mbMode from cur.kind, the fight arena and its radii, proxies; per-fight chapter state
scoreboard players set #mbMode mb 0
execute if data storage rlk:mboss cur{kind:"chapter"} run scoreboard players set #mbMode mb 1
execute store result score #mbAr mb run data get storage rlk:mboss cur.ar
execute if score #mbAr mb matches 0 run scoreboard players set #mbArW10 mb 210
execute if score #mbAr mb matches 0 run scoreboard players set #mbArS10 mb 190
execute if score #mbAr mb matches 1 run scoreboard players set #mbArW10 mb 280
execute if score #mbAr mb matches 1 run scoreboard players set #mbArS10 mb 260
execute if score #mbAr mb matches 2 run scoreboard players set #mbArW10 mb 260
execute if score #mbAr mb matches 2 run scoreboard players set #mbArS10 mb 240
execute if score #mbAr mb matches 9 run scoreboard players set #mbArW10 mb 110
execute if score #mbAr mb matches 9 run scoreboard players set #mbArS10 mb 90
execute store result score #mbPx mb run data get storage rlk:mboss cur.px
scoreboard players set #mbLost mb 0
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
scoreboard players set #mbCine mb 0
scoreboard players set #mbPoolPct mb 100
scoreboard players set #mbRamp mb 0
scoreboard players set #mbHitEv mb 0
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
scoreboard players set #mbPart mb 0
scoreboard players set #mbQi mb 0
data remove storage rlk:mboss lv
data remove storage rlk:mboss px
data remove storage rlk:mboss push
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
data modify storage rlk:mboss aura set value []
scoreboard players set #mbAuraK mb -1
function rlk:mboss/player_reset
function rlk:mboss/opts_reset
