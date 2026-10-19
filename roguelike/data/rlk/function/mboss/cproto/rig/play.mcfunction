# {c} (@s = body): play clip c from its start next rig tick (tick -1 = queued: the proxies keep their offsets).
$scoreboard players set @s mbS $(c)
scoreboard players set @s mbT -1
