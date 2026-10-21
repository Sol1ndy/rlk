# 종말의 여파 (aftermath, id 32; plan 8.3 Q2 / 7.8).
# tick: the approach (#apq32 < 0), the dome models' clips (om/dome/tick), then the clip timeline.
scoreboard players operation #apq32 mb = #apPT mb
scoreboard players operation #apq32 mb -= #apq32S mb
execute if score #apq32 mb matches ..-1 if score #apPT mb matches 8 run function rlk:boss/apep/play/walk_p3
execute if score #apq32 mb matches ..-1 if score #apPT mb matches 8.. run function rlk:boss/apep/p/aftermath/walk
execute if score #apq32 mb matches 54..195 run function rlk:boss/apep/om/dome/tick
execute if score #apq32 mb matches 224.. run return run function rlk:boss/apep/p/aftermath/done
execute if score #apq32 mb matches 0..111 run return run function rlk:boss/apep/p/aftermath/kd/0_111
execute if score #apq32 mb matches 112..196 run return run function rlk:boss/apep/p/aftermath/kd/112_196
