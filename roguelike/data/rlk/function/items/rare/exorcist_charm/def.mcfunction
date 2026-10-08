# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.exorcist_charm set value {item:"minecraft:paper",name:"퇴마의 부적",type:"accessory",rarity:"rare",stats:{atkPct:8},abilities:[{text:"",extra:[{text:"원소전투 스킬을 쓰면 한동안"}]},{text:"",extra:[{text:"기본 공격에 얼음 원소가 부여된다."}]},{text:""},{text:"",extra:[{text:"지속 시간: "},{text:"8초",color:"#FFE08A"}]}],desc:["아이스크림을 먹으면 진정된다."],engravings:["frost","flurry"]}
data modify storage rlk:items ids append value "exorcist_charm"
