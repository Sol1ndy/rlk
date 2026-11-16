# @s = body, every 4 t: the recolour wave (props whose delay ran out take the look) and the ambience.
execute if score #azArT mb matches 1.. run function rlk:boss/azhdaha/arena/wave
execute store result score #azX mb run random value 0..4
execute if score #azX mb matches 0 run function rlk:boss/azhdaha/arena/ambient
