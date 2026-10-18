# Third line: what the device is doing. While the meter is open the core writes only the running field
# pattern ("패턴  <label>") and the kit's put_sub appends the meter: badge, 역장, the 20 pips in groups of five
# (the newest one white for 4 t), the "n/20" digits and the first field's hint (font rlk:mboss_fg).
execute if score #mbSt mb matches 0 run data modify storage rlk:mboss sub set value []
execute if score #mbSt mb matches 0 run return 0
data modify storage rlk:mboss sub set value [{text:"순항",color:"#E8C46A",bold:true}]
execute if score #fgField mb matches 1.. run data modify storage rlk:mboss sub set value [{text:"역장",color:"#C58BFF",bold:true}]
execute if score #fgOpen mb matches 1 run data modify storage rlk:mboss sub set value []
execute if score #fgSt mb matches 1 if score #fgPat mb matches 1 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·일점 상쇄",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 2 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"내려찍기",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 3 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·코어",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 4 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·바위 폭탄",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 5 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·지면 충격",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 6 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·파쇄",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 11 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·감소 영역",color:"#C9B8F5"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 12 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"중력 시스템·파쇄",color:"#C9B8F5"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 21 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"「인력 충격파」",color:"#C9B8F5"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 20 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"역장 생성",color:"#F2E2B0"}]
execute if score #fgSt mb matches 1 if score #fgPat mb matches 22 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"역장 해제",color:"#C9B8F5"}]
execute if score #fgSt mb matches 6 run data modify storage rlk:mboss sub set value [{text:"",font:"rlk:mboss_fg",color:"white"},{text:" 역장 붕괴",color:"#FFE7A0",bold:true}]
execute if score #fgSt mb matches 3 run data modify storage rlk:mboss sub set value [{text:"그로기  ",color:"#9FE8A0",bold:true},{text:"공격할 기회",color:"#C8E8C8"}]
execute if score #fgSt mb matches 4 run data modify storage rlk:mboss sub set value [{text:"그로기  ",color:"#9FE8A0",bold:true},{text:"다시 떠오른다",color:"#C8E8C8"}]
execute if score #fgOpen mb matches 1 run function rlk:mboss/fieldgen/fx/hud/put_sub
