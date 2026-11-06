# Release the forceload of the box of hr_field; a running job of hr_field is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"hr_field"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 832 -40 928 56
