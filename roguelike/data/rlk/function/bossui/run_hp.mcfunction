# #len bu px of colour $(col) on the hp row.
$execute if score #len bu matches 128.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 128.. run scoreboard players remove #len bu 128
$execute if score #len bu matches 64.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 64.. run scoreboard players remove #len bu 64
$execute if score #len bu matches 32.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 32.. run scoreboard players remove #len bu 32
$execute if score #len bu matches 16.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 16.. run scoreboard players remove #len bu 16
$execute if score #len bu matches 8.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 8.. run scoreboard players remove #len bu 8
$execute if score #len bu matches 4.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 4.. run scoreboard players remove #len bu 4
$execute if score #len bu matches 2.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 2.. run scoreboard players remove #len bu 2
$execute if score #len bu matches 1.. run data modify storage rlk:bu line append value {text:"",font:"rlk:bossbar",color:"$(col)"}
execute if score #len bu matches 1.. run scoreboard players remove #len bu 1
