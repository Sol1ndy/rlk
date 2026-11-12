# {ph} (int 0..9): play the registry track cur.music."<ph>" (record category, at each player, non-positional stereo
# event); 0 or no such phase stops the music. Looped by music/tick when len >= 1; vanilla music is stopped every 100 t.
$scoreboard players set #t mb $(ph)
execute unless score #t mb matches 1..9 run return run function rlk:mboss/music/stop
$execute unless data storage rlk:mboss cur.music."$(ph)".ev run return run function rlk:mboss/music/stop
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
$data modify storage rlk:mboss mus set value {ph:$(ph),ev:"",len:0}
$data modify storage rlk:mboss mus.ev set from storage rlk:mboss cur.music."$(ph)".ev
$data modify storage rlk:mboss mus.len set from storage rlk:mboss cur.music."$(ph)".len
$scoreboard players set #mbMusPh mb $(ph)
scoreboard players set #mbMusT mb 0
execute store result score #mbMusLen mb run data get storage rlk:mboss mus.len
function rlk:mboss/music/play with storage rlk:mboss mus
