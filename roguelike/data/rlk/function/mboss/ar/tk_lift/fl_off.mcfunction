# Release the forceload of the box of tk_lift; a running job of tk_lift is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"tk_lift"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 600 -32 680 48
