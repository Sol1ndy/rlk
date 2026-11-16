# (macro ev) the track from its start, at every player (record category, volume 1): vanilla background music stops.
stopsound @a[tag=player] music
$execute as @a[tag=player] at @s run playsound $(ev) record @s ~ ~ ~ 1 1 1
