# GENERATED: the resume hook of the running pattern.
execute if score #apPid mb matches 2 unless score #apPNew mb matches 1 run function rlk:boss/apep/p/hands/resume
execute if score #apPid mb matches 4 unless score #apPNew mb matches 1 run function rlk:boss/apep/p/wither/resume
