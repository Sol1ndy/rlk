# Next action, only here (a pattern boundary). Test request > lock 1-6 (cruise pattern only) > the field
# stage (1 finish the opening, 2 the opening waves, 4 the closing waves, 5 the pack-up) > lock 11-12 (that
# field pattern only, after a normal field opening) / 17 (the field cycle only) > field patterns (until 400 t
# of them, then the closing waves) > cruise (after 5 cruise patterns, later 4: the field).
execute if score #fgPat mb matches 1.. run return 0
execute unless score #fgMv mb matches 0 run function rlk:mboss/fieldgen/ai/mv0
execute if score #fgReq mb matches 1.. run return run function rlk:mboss/fieldgen/ai/req
execute if score #mbLock mb matches 1..6 run return run function rlk:mboss/fieldgen/ai/lock_c
execute if score #fgField mb matches 1 run return run function rlk:mboss/fieldgen/field/up
execute if score #fgField mb matches 2 run return run function rlk:mboss/fieldgen/ai/waves_open
execute if score #fgField mb matches 4 run return run function rlk:mboss/fieldgen/ai/waves_close
execute if score #fgField mb matches 5 run return run function rlk:mboss/fieldgen/ai/pack
execute if score #mbLock mb matches 11..12 run return run function rlk:mboss/fieldgen/ai/lock_f
execute if score #mbLock mb matches 17 run return run function rlk:mboss/fieldgen/ai/lock_cycle
execute if score #fgField mb matches 3 run return run function rlk:mboss/fieldgen/ai/next_f
function rlk:mboss/fieldgen/ai/next_c
