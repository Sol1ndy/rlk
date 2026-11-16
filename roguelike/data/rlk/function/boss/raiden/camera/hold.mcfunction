# No camera lock any more (만겁 footage version, free camera). view/tick calls this while @s (a player) has rdCam 1,
# which only a fight saved by an older build can leave behind: drop the flag and the camera seat.
scoreboard players set @s rdCam 0
ride @s dismount
