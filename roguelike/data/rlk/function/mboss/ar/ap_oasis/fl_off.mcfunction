# Release the forceload of the box of ap_oasis; a running job of ap_oasis is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"ap_oasis"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 396 -36 484 52
