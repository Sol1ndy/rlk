# Q2 (plan 8.3 B0; AP-I2 RP3-2): the two-segment countdown: red (code 2) from the banner to the blast (aftermath
# clip t156), then gold (code 8) to the dome pop (t189). #apq32 = the clip tick (negative on the
# approach), #apq32S = the pattern tick the clip starts on.
execute if score #apq32 mb matches 156.. run return run function rlk:boss/apep/hud/bar_q2g
scoreboard players set #buSub bu 156
scoreboard players operation #buSub bu -= #apq32 mb
scoreboard players set #buSubMax bu 156
scoreboard players operation #buSubMax bu += #apq32S mb
execute if score #buSub bu > #buSubMax bu run scoreboard players operation #buSub bu = #buSubMax bu
scoreboard players set #buSubCol bu 2
