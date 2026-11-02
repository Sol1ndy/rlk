# Release the forceload of the box of fl_ruins; a running job of fl_ruins is aborted first (without the chunks it
# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).
execute if data storage rlk:mboss arjob{aid:"fl_ruins"} run function rlk:mboss/arena/abort
execute in minecraft:overworld run forceload remove 712 -40 808 56
