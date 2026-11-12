# Air over the box of hr_field when it is loaded (room/remove -> cb/remove), and no stamp (no look record).
execute if data storage rlk:mboss arjob{aid:"hr_field"} run function rlk:mboss/arena/abort
data remove storage rlk:mboss built_hr_field
data remove storage rlk:mboss look_hr_field
execute unless function rlk:mboss/ar/hr_field/loaded run return fail
fill 832 190 -40 928 192 56 minecraft:air strict
fill 832 193 -40 928 195 56 minecraft:air strict
fill 832 196 -40 928 198 56 minecraft:air strict
fill 832 199 -40 928 201 56 minecraft:air strict
fill 832 202 -40 928 204 56 minecraft:air strict
fill 832 205 -40 928 207 56 minecraft:air strict
fill 832 208 -40 928 210 56 minecraft:air strict
fill 832 211 -40 928 213 56 minecraft:air strict
fill 832 214 -40 928 216 56 minecraft:air strict
fill 832 217 -40 928 219 56 minecraft:air strict
fill 832 220 -40 928 222 56 minecraft:air strict
fill 832 223 -40 928 225 56 minecraft:air strict
fill 832 226 -40 928 228 56 minecraft:air strict
fill 832 229 -40 928 231 56 minecraft:air strict
fill 832 232 -40 928 234 56 minecraft:air strict
fill 832 235 -40 928 237 56 minecraft:air strict
fill 832 238 -40 928 240 56 minecraft:air strict
fill 832 241 -40 928 243 56 minecraft:air strict
fill 832 244 -40 928 246 56 minecraft:air strict
fill 832 247 -40 928 249 56 minecraft:air strict
fill 832 250 -40 928 250 56 minecraft:air strict
return 1
