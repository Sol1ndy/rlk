# function rlk:boss/apep/om/stalk/play {i:<0..3>,clip:"<clip>"}.
$scoreboard players set #apOmI mb $(i)
$data modify storage rlk:mboss apomc set value "$(clip)"
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"leg_rise"} run return run function rlk:boss/apep/om/stalk/i0/play/leg_rise
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"leg_slam"} run return run function rlk:boss/apep/om/stalk/i0/play/leg_slam
execute if score #apOmI mb matches 0 if data storage rlk:mboss {apomc:"leg_sink"} run return run function rlk:boss/apep/om/stalk/i0/play/leg_sink
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"leg_rise"} run return run function rlk:boss/apep/om/stalk/i1/play/leg_rise
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"leg_slam"} run return run function rlk:boss/apep/om/stalk/i1/play/leg_slam
execute if score #apOmI mb matches 1 if data storage rlk:mboss {apomc:"leg_sink"} run return run function rlk:boss/apep/om/stalk/i1/play/leg_sink
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"leg_rise"} run return run function rlk:boss/apep/om/stalk/i2/play/leg_rise
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"leg_slam"} run return run function rlk:boss/apep/om/stalk/i2/play/leg_slam
execute if score #apOmI mb matches 2 if data storage rlk:mboss {apomc:"leg_sink"} run return run function rlk:boss/apep/om/stalk/i2/play/leg_sink
execute if score #apOmI mb matches 3 if data storage rlk:mboss {apomc:"leg_rise"} run return run function rlk:boss/apep/om/stalk/i3/play/leg_rise
execute if score #apOmI mb matches 3 if data storage rlk:mboss {apomc:"leg_slam"} run return run function rlk:boss/apep/om/stalk/i3/play/leg_slam
execute if score #apOmI mb matches 3 if data storage rlk:mboss {apomc:"leg_sink"} run return run function rlk:boss/apep/om/stalk/i3/play/leg_sink
