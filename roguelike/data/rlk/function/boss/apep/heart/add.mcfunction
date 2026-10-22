# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# Macro {v}: progress + v (clamp 10000; the stage tick starts the CS at 10000): the gain swell, the sparkle and
# the chime (its pitch rises with the progress: #apHt first, requests/fx.md RFX-2).
$scoreboard players add #apHt mb $(v)
execute if score #apHt mb matches 10001.. run scoreboard players set #apHt mb 10000
execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/heart_gain
execute positioned 440 202.6 8 run function rlk:boss/apep/fx/snd/heart_gain
execute if score #apStage mb matches 1 if entity 524c4b4d-4150-4800-8000-000000000000 run function rlk:boss/apep/om/heart/play/heart_gain
scoreboard players set #apHudQ mb 1
