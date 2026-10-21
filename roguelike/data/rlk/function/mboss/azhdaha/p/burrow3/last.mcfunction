# HP 1 at the surfacing: "마지막 일격!" (the next hit kills through the normal path); a gold glow on the
# body (the gold parts lit) and gold motes at every hit proxy.
scoreboard players set #azLastHit mb 1
scoreboard players set #azHudQ mb 1
function rlk:mboss/azhdaha/rig/glow/gold_on
execute as @e[tag=rlk_mb_px] at @s run particle minecraft:wax_on ~ ~1 ~ 0.4 0.8 0.4 0 6 force @a[tag=player]
function rlk:mboss/azhdaha/fx/snd/hint
