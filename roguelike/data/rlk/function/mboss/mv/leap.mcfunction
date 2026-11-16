# Like glide, with a parabolic arc of apex h (tenths of a block above the straight path).
function rlk:mboss/mv/setup
$scoreboard players set @s mbMvN $(t)
$scoreboard players set @s mbMvH $(h)
scoreboard players operation @s mbMvH *= #c100 mb
