execute if score #skillDmg tmp matches 1 run scoreboard players operation #chainT eng = #chainDur tmp
execute if score #basic itv matches 1 unless score #sub itv matches 1 if score #chainT eng matches 1.. run scoreboard players operation #eb eng += #chainBasic tmp
