# Q2 (plan 7.4): first after 1 phase-3 pattern(s); then >= 900 t after the last and >= 3
# other patterns; never before #apAftCd (a cancel: +300 t). Returns 1 when due.
execute if score #apFc mb < #apAftCd mb run return fail
execute if score #apAft1 mb matches 0 if score #apP3N mb matches 1.. run return 1
execute if score #apAft1 mb matches 1 if score #apAftN mb matches 3.. run return 1
return fail
