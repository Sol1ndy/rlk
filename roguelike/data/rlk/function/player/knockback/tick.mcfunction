# @s = rlk_plkb marker. Its horizontal facing is the recoil direction.
# pkbT is the number of 0.1-block steps this tick, decaying by one each tick.
execute unless entity @a[tag=player,limit=1] run return run kill @s
execute unless entity @e[tag=rlk_body,limit=1] run return run kill @s
execute if entity @a[tag=player,scores={dead=1..}] run return run kill @s
execute if entity @a[tag=player,scores={curHealth=..0}] run return run kill @s
execute if entity @a[tag=player,scores={rnDie=1..}] run return run kill @s
execute if entity @a[tag=player,scores={pkMode=1..}] run return run kill @s
execute if entity @a[tag=player,scores={vMap=1..}] run return run kill @s
execute if entity @a[tag=player,scores={dashInvT=1..}] run return run kill @s
execute if entity @a[tag=player,scores={dashMoveT=1..}] run return run kill @s
execute unless score @s pkbT matches 1.. run return run kill @s
scoreboard players operation #pkbSteps tmp = @s pkbT
scoreboard players set #pkbBlocked tmp 0
function rlk:player/knockback/step
# A blocked step already removed this marker. Do not touch it again.
execute if score #pkbBlocked tmp matches 1 run return 0
scoreboard players remove @s pkbT 1
execute if score @s pkbT matches ..0 run kill @s
