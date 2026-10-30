# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# Macro {v}: progress - v (clamp 0; the stage tick starts the failure strike at 0): the flinch, red-gold motes,
# the hit sound. (The bossui's white recent-loss trail shows the loss by itself.)
$scoreboard players remove #apHt mb $(v)
execute if score #apHt mb matches ..-1 run scoreboard players set #apHt mb 0
execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/heart_hit
execute positioned 440 202.6 8 run function rlk:boss/apep/fx/snd/heart_hit
execute if score #apStage mb matches 1 if entity 524c4b4d-4150-4800-8000-000000000000 run function rlk:boss/apep/om/heart/play/heart_hit
scoreboard players set #apHudQ mb 1
