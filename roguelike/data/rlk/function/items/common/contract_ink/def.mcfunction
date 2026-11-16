# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.contract_ink set value {item:"minecraft:black_dye",name:"계약의 잉크",type:"accessory",rarity:"common",stats:{atkPct:6},abilities:[{text:"",extra:[{text:"원소전투 스킬을 쓰면 생명의 계약을 얻는다."}]},{text:"",extra:[{text:"(생명의 계약: 받는 치유를 대신 흡수하는 빚)"}]},{text:""},{text:"",extra:[{text:"생명의 계약: "},{text:"최대 체력의 ",color:"#FFE08A"},{tk:{c:"#inkBol",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]}],desc:["서명은 한 번, 대가는 오래."],engravings:["pact","berserk"]}
data modify storage rlk:items ids append value "contract_ink"
