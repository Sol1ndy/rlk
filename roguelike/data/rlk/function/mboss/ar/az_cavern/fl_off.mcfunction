# Release the forceload of the box of az_cavern; a running job of az_cavern is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"az_cavern"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 280 -32 360 48
