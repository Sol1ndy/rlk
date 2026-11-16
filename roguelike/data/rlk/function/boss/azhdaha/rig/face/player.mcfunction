# Turn the anchor to face the nearest player (yaw only). @s = rig anchor.
execute facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
