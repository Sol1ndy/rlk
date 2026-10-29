# From room/clear (map change, run end, death, room/wipe): the rift entities went with rlk_room, so the tick
# stops. (#riftUsed stays: once per run; #riftForce stays armed until a zone takes it.)
scoreboard players set #riftOn room 0
