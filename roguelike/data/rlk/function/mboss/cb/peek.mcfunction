# Optional (cm.md 5.10): rlk:mboss cbpeek = the chapter boss the boss map of #chapter room routes to (none = Raiden).
data remove storage rlk:mboss cbpeek
execute if score #chapter room matches 1 run return run data modify storage rlk:mboss cbpeek set value {id:"azhdaha",name:"야타용왕",color:"#F2B53A"}
execute if score #chapter room matches 3 run return run data modify storage rlk:mboss cbpeek set value {id:"apep",name:"아펩의 오아시스 파수꾼",color:"#C9C452"}
