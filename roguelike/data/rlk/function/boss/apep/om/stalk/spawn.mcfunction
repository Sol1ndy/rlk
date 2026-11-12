# function rlk:boss/apep/om/stalk/spawn {i:<0..3>} at the stalk spot, rotated as wanted.
$scoreboard players set #apOmI mb $(i)
execute if score #apOmI mb matches 0 run return run function rlk:boss/apep/om/stalk/i0/spawn
execute if score #apOmI mb matches 1 run return run function rlk:boss/apep/om/stalk/i1/spawn
execute if score #apOmI mb matches 2 run return run function rlk:boss/apep/om/stalk/i2/spawn
execute if score #apOmI mb matches 3 run return run function rlk:boss/apep/om/stalk/i3/spawn
