# Start (or restart) the sliced Plane of Euthymia backdrop: #rdBgI rd = next slice (-1 aborted, 20 done).
scoreboard players set #rdBgI rd 0
scoreboard players set #rdBgW rd 0
schedule function rlk:room/raiden/bg/tick 1t replace
