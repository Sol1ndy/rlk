# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치". '○○ 원소 피해' 문구는 그 원소 색
data modify storage rlk:items registry.sealed_sword set value {item:"minecraft:obsidian",name:"봉인된 검",type:"accessory",rarity:"epic",stats:{atkPct:15},abilities:[{text:"",extra:[{text:"적을 처치할 때마다 처치 수가 쌓인다."}]},{text:"",extra:[{text:"처치 수를 다 채우면 이 아이템은 마검: 키리온으로 변한다."}]},{text:""},{text:"",extra:[{text:"필요 처치 수: "},{text:"150",color:"#FFE08A"}]}],desc:["강력한 힘으로 억제되어 있는 검."]}
data modify storage rlk:items ids append value "sealed_sword"
