# Optional (cm.md 5.10): rlk:mboss cbpeek = the chapter boss the boss map of #chapter room routes to (none = Raiden).
data remove storage rlk:mboss cbpeek
execute if score #chapter room matches 1 run return run data modify storage rlk:mboss cbpeek set value {id:"azhdaha",name:"야타용왕",color:"#F2B53A"}
