# Release the forceload of the box of cp_test; a running job of cp_test is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"cp_test"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 524 -8 556 24
