# Hook resume: every active pattern's resume; a running Q2 is cancelled (domes removed, 300 t; plan
# 7.2); phase 2: rev/resume.
function rlk:boss/apep/p/resume_d
execute if score #apPid mb matches 32 run function rlk:boss/apep/aft/cancel
execute if score #apPh mb matches 2 run function rlk:boss/apep/rev/resume
