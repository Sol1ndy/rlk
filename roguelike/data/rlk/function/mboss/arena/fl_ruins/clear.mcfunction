# Air over the box of fl_ruins when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"fl_ruins"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_fl_ruins
data remove storage rlk:mboss look_fl_ruins
execute unless function rlk:mboss/ar/fl_ruins/loaded run return fail
fill 712 190 -40 808 192 56 minecraft:air strict
fill 712 193 -40 808 195 56 minecraft:air strict
fill 712 196 -40 808 198 56 minecraft:air strict
fill 712 199 -40 808 201 56 minecraft:air strict
fill 712 202 -40 808 204 56 minecraft:air strict
fill 712 205 -40 808 207 56 minecraft:air strict
fill 712 208 -40 808 210 56 minecraft:air strict
fill 712 211 -40 808 213 56 minecraft:air strict
fill 712 214 -40 808 216 56 minecraft:air strict
fill 712 217 -40 808 219 56 minecraft:air strict
fill 712 220 -40 808 222 56 minecraft:air strict
fill 712 223 -40 808 225 56 minecraft:air strict
fill 712 226 -40 808 228 56 minecraft:air strict
fill 712 229 -40 808 231 56 minecraft:air strict
fill 712 232 -40 808 234 56 minecraft:air strict
fill 712 235 -40 808 237 56 minecraft:air strict
fill 712 238 -40 808 240 56 minecraft:air strict
fill 712 241 -40 808 243 56 minecraft:air strict
fill 712 244 -40 808 246 56 minecraft:air strict
fill 712 247 -40 808 249 56 minecraft:air strict
fill 712 250 -40 808 250 56 minecraft:air strict
return 1
