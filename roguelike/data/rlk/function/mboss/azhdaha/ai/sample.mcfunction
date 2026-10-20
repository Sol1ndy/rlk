# @s = body (every 4 t and at every pick): the player in the anchor frame (#mbLf / #mbLs, mb), the zone, the band,
# the side, the nearest paw, the FLANK-near flag and the dwell ring, the P7 exit test, the P3 front cone, anchor8.
function rlk:mboss/mv/local
function rlk:mboss/mv/dist
scoreboard players operation #azDist mb = #mbDist mb
scoreboard players operation #azF mb = #mbLf mb
scoreboard players operation #azS mb = #mbLs mb
scoreboard players operation #azAs mb = #azS mb
execute if score #azAs mb matches ..-1 run scoreboard players operation #azAs mb *= #cm1 mb
scoreboard players set #azSide mb 1
execute if score #azS mb matches ..-1 run scoreboard players set #azSide mb -1
# band by the anchor distance (tenths)
scoreboard players set #azBand mb 2
execute if score #azDist mb matches ..90 run scoreboard players set #azBand mb 1
execute if score #azDist mb matches 151.. run scoreboard players set #azBand mb 3
# tenths for the squares (no int overflow)
scoreboard players operation #azFt mb = #azF mb
scoreboard players operation #azFt mb /= #c100 mb
scoreboard players operation #azSt mb = #azS mb
scoreboard players operation #azSt mb /= #c100 mb
scoreboard players set #azPawD2 mb 999999
scoreboard players set #azPaw mb 1
scoreboard players operation #azX mb = #azSt mb
scoreboard players remove #azX mb 32
scoreboard players operation #azX mb *= #azX mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players remove #azY mb 24
scoreboard players operation #azY mb *= #azY mb
scoreboard players operation #azX mb += #azY mb
execute if score #azX mb < #azPawD2 mb run scoreboard players set #azPaw mb 1
execute if score #azX mb < #azPawD2 mb run scoreboard players operation #azPawD2 mb = #azX mb
scoreboard players operation #azX mb = #azSt mb
scoreboard players remove #azX mb -32
scoreboard players operation #azX mb *= #azX mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players remove #azY mb 24
scoreboard players operation #azY mb *= #azY mb
scoreboard players operation #azX mb += #azY mb
execute if score #azX mb < #azPawD2 mb run scoreboard players set #azPaw mb 2
execute if score #azX mb < #azPawD2 mb run scoreboard players operation #azPawD2 mb = #azX mb
scoreboard players operation #azX mb = #azSt mb
scoreboard players remove #azX mb 25
scoreboard players operation #azX mb *= #azX mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players remove #azY mb -29
scoreboard players operation #azY mb *= #azY mb
scoreboard players operation #azX mb += #azY mb
execute if score #azX mb < #azPawD2 mb run scoreboard players set #azPaw mb 3
execute if score #azX mb < #azPawD2 mb run scoreboard players operation #azPawD2 mb = #azX mb
scoreboard players operation #azX mb = #azSt mb
scoreboard players remove #azX mb -25
scoreboard players operation #azX mb *= #azX mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players remove #azY mb -29
scoreboard players operation #azY mb *= #azY mb
scoreboard players operation #azX mb += #azY mb
execute if score #azX mb < #azPawD2 mb run scoreboard players set #azPaw mb 4
execute if score #azX mb < #azPawD2 mb run scoreboard players operation #azPawD2 mb = #azX mb
# the head cone: f >= 3.6 and 10|s| <= 10 x 4 + 6 (f - 3.6) (blocks x 1000)
scoreboard players set #azHd mb 0
scoreboard players operation #azX mb = #azF mb
scoreboard players remove #azX mb 3600
scoreboard players set #azY mb 6
scoreboard players operation #azX mb *= #azY mb
scoreboard players add #azX mb 40000
scoreboard players operation #azY mb = #azAs mb
scoreboard players operation #azY mb *= #c10 mb
execute if score #azF mb matches 3600.. if score #azY mb <= #azX mb run scoreboard players set #azHd mb 1
# the zone: PAW first (2.8 b of a paw / foot, or under the body), HEAD, TAIL, FLANK
scoreboard players set #azZone mb 5
execute if score #azAs mb matches ..9000 run scoreboard players set #azZone mb 4
execute if score #azF mb matches ..-4801 if score #azAs mb matches ..3500 run scoreboard players set #azZone mb 6
execute if score #azF mb matches ..-4801 if score #azAs mb matches 3501.. run scoreboard players set #azZone mb 7
execute if score #azHd mb matches 1 run scoreboard players operation #azZone mb = #azBand mb
execute if score #azPawD2 mb matches ..784 run scoreboard players set #azZone mb 8
execute if score #azAs mb matches ..2999 if score #azF mb matches -4800..3599 run scoreboard players set #azZone mb 8
# the FLANK-near test of the rule (plan 4.12, independent of the PAW precedence)
scoreboard players set #azFN mb 0
execute if score #azAs mb matches 3000..9000 if score #azF mb matches -4800..3599 run scoreboard players set #azFN mb 1
# within +-45 degrees of the front (idle tracking) and the turn step kind
scoreboard players set #azF45 mb 0
execute if score #azF mb >= #azAs mb run scoreboard players set #azF45 mb 1
# the P3 cone: within +-35 degrees: f > 0 and 10000 |s| <= 7002 f
scoreboard players set #azF35 mb 0
scoreboard players operation #azX mb = #azSt mb
execute if score #azX mb matches ..-1 run scoreboard players operation #azX mb *= #cm1 mb
scoreboard players set #azY mb 10000
scoreboard players operation #azX mb *= #azY mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players set #azZ mb 7002
scoreboard players operation #azY mb *= #azZ mb
execute if score #azFt mb matches 1.. if score #azX mb <= #azY mb run scoreboard players set #azF35 mb 1
function rlk:mboss/azhdaha/ai/exit
# anchor8: the anchor within 8 b of the arena centre
scoreboard players set #azA8 mb 0
execute at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..8,limit=1] run scoreboard players set #azA8 mb 1
