# The field is over (the pack-up, the break, a reload, a test): the kit's meter, low-gravity icon and hint
# leave the lines (only the flags still on: each kit call rebuilds its components; the caller refreshes
# the lines).
execute if data storage rlk:fgkit hud{open:1b} run function rlk:mboss/fieldgen/fx/hud/meter_close
execute if data storage rlk:fgkit hud{lowg:1b} run function rlk:mboss/fieldgen/fx/hud/lowg_off
execute if data storage rlk:fgkit hud{hint:1b} run function rlk:mboss/fieldgen/fx/hud/hint_off
