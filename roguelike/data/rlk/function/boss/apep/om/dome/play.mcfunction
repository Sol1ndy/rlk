# function rlk:boss/apep/om/dome/play {i:<0..2>,clip:"<clip>"}.
$scoreboard players set #apOmI mb $(i)
$data modify storage rlk:mboss apomc set value "$(clip)"
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"dome_rise"} run return run function rlk:boss/apep/om/dome/i0/play/dome_rise
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"dome_idle"} run return run function rlk:boss/apep/om/dome/i0/play/dome_idle
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"dome_pop"} run return run function rlk:boss/apep/om/dome/i0/play/dome_pop
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"dome_rise"} run return run function rlk:boss/apep/om/dome/i1/play/dome_rise
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"dome_idle"} run return run function rlk:boss/apep/om/dome/i1/play/dome_idle
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"dome_pop"} run return run function rlk:boss/apep/om/dome/i1/play/dome_pop
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"dome_rise"} run return run function rlk:boss/apep/om/dome/i2/play/dome_rise
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"dome_idle"} run return run function rlk:boss/apep/om/dome/i2/play/dome_idle
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"dome_pop"} run return run function rlk:boss/apep/om/dome/i2/play/dome_pop
