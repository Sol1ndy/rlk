# Air over the box of ap_oasis when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"ap_oasis"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_ap_oasis
data remove storage rlk:mboss look_ap_oasis
execute unless function rlk:mboss/ar/ap_oasis/loaded run return fail
fill 396 190 -36 484 193 52 minecraft:air strict
fill 396 194 -36 484 197 52 minecraft:air strict
fill 396 198 -36 484 201 52 minecraft:air strict
fill 396 202 -36 484 205 52 minecraft:air strict
fill 396 206 -36 484 209 52 minecraft:air strict
fill 396 210 -36 484 213 52 minecraft:air strict
fill 396 214 -36 484 217 52 minecraft:air strict
fill 396 218 -36 484 221 52 minecraft:air strict
fill 396 222 -36 484 224 52 minecraft:air strict
fill 396 225 -36 484 226 52 minecraft:air strict
fill 396 227 -36 484 228 52 minecraft:air strict
fill 396 229 -36 484 230 52 minecraft:air strict
fill 396 231 -36 484 232 52 minecraft:air strict
fill 396 233 -36 484 234 52 minecraft:air strict
fill 396 235 -36 484 236 52 minecraft:air strict
fill 396 237 -36 484 238 52 minecraft:air strict
fill 396 239 -36 484 240 52 minecraft:air strict
fill 396 241 -36 484 242 52 minecraft:air strict
fill 396 243 -36 484 244 52 minecraft:air strict
fill 396 245 -36 484 246 52 minecraft:air strict
fill 396 247 -36 484 248 52 minecraft:air strict
fill 396 249 -36 484 250 52 minecraft:air strict
return 1
