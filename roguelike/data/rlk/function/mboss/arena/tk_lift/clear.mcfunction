# Air over the box of tk_lift when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"tk_lift"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_tk_lift
data remove storage rlk:mboss look_tk_lift
execute unless function rlk:mboss/ar/tk_lift/loaded run return fail
fill 600 190 -32 680 193 48 minecraft:air strict
fill 600 194 -32 680 197 48 minecraft:air strict
fill 600 198 -32 680 201 48 minecraft:air strict
fill 600 202 -32 680 205 48 minecraft:air strict
fill 600 206 -32 680 209 48 minecraft:air strict
fill 600 210 -32 680 213 48 minecraft:air strict
fill 600 214 -32 680 217 48 minecraft:air strict
fill 600 218 -32 680 221 48 minecraft:air strict
fill 600 222 -32 680 225 48 minecraft:air strict
fill 600 226 -32 680 229 48 minecraft:air strict
fill 600 230 -32 680 233 48 minecraft:air strict
fill 600 234 -32 680 237 48 minecraft:air strict
fill 600 238 -32 680 241 48 minecraft:air strict
fill 600 242 -32 680 245 48 minecraft:air strict
fill 600 246 -32 680 249 48 minecraft:air strict
fill 600 250 -32 680 250 48 minecraft:air strict
return 1
