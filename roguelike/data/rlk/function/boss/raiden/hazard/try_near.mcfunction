# @s = a dodgeable hazard that missed the body in the perfect-dodge window: hit / land with the body mark and the cached
# body position on the dodge's start (player/def/ghost_on; nothing when it is gone), then both back.
function rlk:player/def/ghost_on
execute unless score #gh cb matches 1 run return 0
scoreboard players operation #rdNX rd = #rdBX rd
scoreboard players operation #rdNY rd = #rdBY rd
scoreboard players operation #rdNZ rd = #rdBZ rd
function rlk:boss/raiden/hazard/body
function rlk:boss/raiden/hazard/hit
execute if score #rdHit rd matches 1 run function rlk:boss/raiden/hazard/land
function rlk:player/def/ghost_off
scoreboard players operation #rdBX rd = #rdNX rd
scoreboard players operation #rdBY rd = #rdNY rd
scoreboard players operation #rdBZ rd = #rdNZ rd
