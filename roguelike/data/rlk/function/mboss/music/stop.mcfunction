# Stop the music (no fade; a sting is the caller's): the sound, #mbMusPh 0, rlk:mboss mus removed.
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
scoreboard players set #mbMusPh mb 0
scoreboard players set #mbMusT mb 0
data remove storage rlk:mboss mus
