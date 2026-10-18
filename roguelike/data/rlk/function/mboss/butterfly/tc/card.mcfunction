# One tinted card at the executing position/rotation (tools/mboss_butterfly/cards.py, api.Gen.tcard: the call is
# execute positioned <pos> rotated <rot> run ...): {kind, bb:fixed|center|vertical|horizontal, roll:<deg>, spin:<deg over the life,
#  -170..170>, s0/s1:<start/end size>, move:"dx,dy,dz" (end offset, display frame), life:<t>, fade:<shrink-out t>,
#  col:<int RGB>, ax:"<spin axis = the card normal>"}. Kinds: star, burst, ring, glow, orb, slash, crescent, moon, shard, leaf, flame, swirl. At most 40 live (further spawns
#  are skipped).
execute if score #bfTcN mb matches 40.. run return 0
scoreboard players add #bfTcN mb 1
$data modify storage rlk:mboss bftc set value {kind:"$(kind)",bb:"$(bb)",s0:$(s0),s1:$(s1),move:"$(move)",col:$(col),ax:"$(ax)",rr:0f,sr:0f,d:1,f:0}
$scoreboard players set #bfTcR mb $(roll)
$scoreboard players set #bfTcS mb $(spin)
$scoreboard players set #bfTcL mb $(life)
$scoreboard players set #bfTcF mb $(fade)
execute if score #bfTcL mb matches ..1 run scoreboard players set #bfTcL mb 2
execute if score #bfTcF mb matches ..-1 run scoreboard players set #bfTcF mb 0
scoreboard players operation #bfTcD mb = #bfTcL mb
scoreboard players remove #bfTcD mb 2
scoreboard players operation #bfTcF mb < #bfTcD mb
execute if score #bfTcS mb matches 171.. run scoreboard players set #bfTcS mb 170
execute if score #bfTcS mb matches ..-171 run scoreboard players set #bfTcS mb -170
scoreboard players operation #bfTcD mb = #bfTcL mb
scoreboard players operation #bfTcD mb -= #bfTcF mb
scoreboard players remove #bfTcD mb 1
execute store result storage rlk:mboss bftc.rr float 0.017453292 run scoreboard players get #bfTcR mb
execute store result storage rlk:mboss bftc.sr float 0.017453292 run scoreboard players get #bfTcS mb
execute store result storage rlk:mboss bftc.d int 1 run scoreboard players get #bfTcD mb
execute store result storage rlk:mboss bftc.f int 1 run scoreboard players get #bfTcF mb
function rlk:mboss/butterfly/tc/spawn with storage rlk:mboss bftc
scoreboard players operation #bfTcT mb = #bfTcNow mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_tcn,limit=1] run function rlk:mboss/butterfly/tc/born
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_tcn] remove rlk_mb_bf_tcn
