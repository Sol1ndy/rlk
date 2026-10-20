# The jump cue: "점프!" on the sub-line 12 t + the bell (plan 5 T1 tells; HUD, not a telegraph).
scoreboard players set #azCue mb 12
function rlk:mboss/azhdaha/fx/hud/cue_jump
function rlk:mboss/azhdaha/fx/snd/jump_cue
execute as @a[tag=player] at @s run playsound minecraft:block.note_block.bell hostile @s ~ ~ ~ 0.9 1.2 0.3
