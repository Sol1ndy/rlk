# 종말의 여파 (aftermath, id 32; plan 8.3 Q2 / 7.8; fix 10-22f).
# tick: the approach (#apq32 < 0), then the clip timeline (the core steps the dome models' clips: obj/tick);
# the B0 clock first (btick: the domes and the field look).
scoreboard players operation #apq32 mb = #apPT mb
scoreboard players operation #apq32 mb -= #apq32S mb
execute if score #apq32 mb matches ..-1 if score #apPT mb matches 8 run function rlk:boss/apep/play/walk_p3
execute if score #apq32 mb matches ..-1 if score #apPT mb matches 8.. run function rlk:boss/apep/p/aftermath/walk
execute if score #apq32 mb matches 224.. run return run function rlk:boss/apep/p/aftermath/done
execute if score #apq32 mb matches ..155 if score #mbHitEv mb > #apq32H mb at @e[tag=rlk_body,limit=1] run function rlk:boss/apep/fx/snd/q2_tick
scoreboard players operation #apq32H mb = #mbHitEv mb
function rlk:boss/apep/p/aftermath/btick
execute if score #apq32 mb matches 0..134 run return run function rlk:boss/apep/p/aftermath/kd/0_134
execute if score #apq32 mb matches 138..196 run return run function rlk:boss/apep/p/aftermath/kd/138_196
