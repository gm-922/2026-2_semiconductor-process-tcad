AdvancedCalibration
puts "CHK default  B DiffModel = [pdbGetSwitchString Silicon Boron DiffModel]"
puts "CHK default  Int Cluster = [pdbGetSwitchString Silicon Int ClusterModel]"
pdbSet Silicon Dopant DiffModel Fermi
puts "CHK TEDoff   B DiffModel = [pdbGetSwitchString Silicon Boron DiffModel]"
puts "CHK TEDoff   Int Cluster = [pdbGetSwitchString Silicon Int ClusterModel]"
exit
