# Core mechanics on the service patterns' clocks (their pattern files own only fx): the field opening (20)
# 0 = the stage, 13 = warp-out (untargetable, to the centre), 34 = warp-in clip, 35 = the unfold
# (the meter opens, targetable), 56 = the banner and low gravity; the pack-up (22) 0 = meter and low gravity off.
execute if score #fgPat mb matches 20 if score #fgPT mb matches 0 run return run function rlk:mboss/fieldgen/field/warp_begin
execute if score #fgPat mb matches 20 if score #fgPT mb matches 13 run return run function rlk:mboss/fieldgen/field/warp
execute if score #fgPat mb matches 20 if score #fgPT mb matches 34 run return run function rlk:mboss/fieldgen/rig_stub/play/warp_in_field
execute if score #fgPat mb matches 20 if score #fgPT mb matches 35 run return run function rlk:mboss/fieldgen/field/open
execute if score #fgPat mb matches 20 if score #fgPT mb matches 56 run return run function rlk:mboss/fieldgen/field/banner
execute if score #fgPat mb matches 22 if score #fgPT mb matches 0 run return run function rlk:mboss/fieldgen/field/close
