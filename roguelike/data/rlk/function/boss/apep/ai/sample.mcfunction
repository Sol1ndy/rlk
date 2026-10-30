# @s = body: the player in the anchor frame (#apF / #apS mb, #apAs = |s|), the distance (#apDist tenths), the
# zone, the band, the weight column, the side, the wide flag (|dyaw| > 60), the rim and centre flags.
function rlk:mboss/mv/local
function rlk:mboss/mv/dist
scoreboard players operation #apDist mb = #mbDist mb
scoreboard players operation #apF mb = #mbLf mb
scoreboard players operation #apS mb = #mbLs mb
scoreboard players operation #apAs mb = #apS mb
execute if score #apAs mb matches ..-1 run scoreboard players operation #apAs mb *= #cm1 mb
scoreboard players set #apSide mb 1
execute if score #apS mb matches ..-1 run scoreboard players set #apSide mb -1
# FRONT cone: f >= 3.0 and 10 |s| <= 10 x 4.0 + 6 (f - 3.0) (mb)
scoreboard players set #apZone mb 2
scoreboard players operation #apX mb = #apF mb
scoreboard players remove #apX mb 3000
scoreboard players set #apY mb 6
scoreboard players operation #apX mb *= #apY mb
scoreboard players add #apX mb 40000
scoreboard players operation #apY mb = #apAs mb
scoreboard players operation #apY mb *= #c10 mb
execute if score #apF mb matches 3000.. if score #apY mb <= #apX mb run scoreboard players set #apZone mb 1
execute if score #apF mb matches -3000..2999 if score #apAs mb matches ..3000 run scoreboard players set #apZone mb 3
execute if score #apF mb matches ..-3001 run scoreboard players set #apZone mb 4
# the band (tenths of the anchor distance; P1 / P3 bounds)
scoreboard players set #apBand mb 2
execute if score #apPh mb matches 1 if score #apDist mb matches ..75 run scoreboard players set #apBand mb 1
execute if score #apPh mb matches 1 if score #apDist mb matches 141.. run scoreboard players set #apBand mb 3
execute if score #apPh mb matches 3 if score #apDist mb matches ..60 run scoreboard players set #apBand mb 1
execute if score #apPh mb matches 3 if score #apDist mb matches 141.. run scoreboard players set #apBand mb 3
# the weight column (phase 1: FRONT x band, SIDE / UNDER, BACK; phase 3: the band)
scoreboard players operation #apCol mb = #apBand mb
execute if score #apPh mb matches 1 if score #apZone mb matches 2..3 run scoreboard players set #apCol mb 4
execute if score #apPh mb matches 1 if score #apZone mb matches 4 run scoreboard players set #apCol mb 5
# wide: |dyaw| > 60 degrees (1000 f < 577 |s|)
scoreboard players set #apWide mb 0
scoreboard players operation #apX mb = #apF mb
scoreboard players operation #apX mb *= #c1000 mb
scoreboard players set #apY mb 577
scoreboard players operation #apY mb *= #apAs mb
execute if score #apX mb < #apY mb run scoreboard players set #apWide mb 1
# rim: the anchor beyond r 12 of the centre; cfree: the player beyond 5 b of the centre
scoreboard players set #apRim mb 0
execute positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run scoreboard players set #apRim mb 1
scoreboard players set #apCFree mb 1
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..5,limit=1] run scoreboard players set #apCFree mb 0
