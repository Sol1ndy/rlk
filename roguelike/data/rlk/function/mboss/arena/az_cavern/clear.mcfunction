# Air over the box of az_cavern when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"az_cavern"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_az_cavern
data remove storage rlk:mboss look_az_cavern
execute unless function rlk:mboss/ar/az_cavern/loaded run return fail
fill 280 190 -32 360 193 48 minecraft:air strict
fill 280 194 -32 360 197 48 minecraft:air strict
fill 280 198 -32 360 201 48 minecraft:air strict
fill 280 202 -32 360 205 48 minecraft:air strict
fill 280 206 -32 360 209 48 minecraft:air strict
fill 280 210 -32 360 213 48 minecraft:air strict
fill 280 214 -32 360 217 48 minecraft:air strict
fill 280 218 -32 360 221 48 minecraft:air strict
fill 280 222 -32 360 225 48 minecraft:air strict
fill 280 226 -32 360 229 48 minecraft:air strict
fill 280 230 -32 360 233 48 minecraft:air strict
fill 280 234 -32 360 237 48 minecraft:air strict
fill 280 238 -32 360 240 48 minecraft:air strict
return 1
