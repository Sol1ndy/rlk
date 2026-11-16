# The core bubble shows the next crack stage (#fgCrack, read by reloads and tests). The kit's meter_hit
# cracks the rig on the counts 5 / 10 / 15; the core does it only for a stage reached another way (test 31).
scoreboard players operation #fgCrack mb = #fgX mb
execute unless score #fgBrk mb matches 5 unless score #fgBrk mb matches 10 unless score #fgBrk mb matches 15 run function rlk:mboss/fieldgen/u/crack_d
