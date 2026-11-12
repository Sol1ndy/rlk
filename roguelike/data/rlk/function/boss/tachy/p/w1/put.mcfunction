# The body to this spot (@s = body; the caller checked mv/ok), facing the player.
execute if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
