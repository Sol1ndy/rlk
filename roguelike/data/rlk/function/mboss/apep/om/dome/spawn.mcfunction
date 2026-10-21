# function rlk:mboss/apep/om/dome/spawn {i:<0..2>} at the dome spot, rotated as wanted.
$scoreboard players set #apOmI mb $(i)
execute if score #apOmI mb matches 0 run return run function rlk:mboss/apep/om/dome/i0/spawn
execute if score #apOmI mb matches 1 run return run function rlk:mboss/apep/om/dome/i1/spawn
execute if score #apOmI mb matches 2 run return run function rlk:mboss/apep/om/dome/i2/spawn
