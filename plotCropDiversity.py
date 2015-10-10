import AgCensus
import AgCensusViz

kfile = open("key.txt")
key = kfile.read().strip()
AgCensus.set_api(key)

area = AgCensus.get_areacropsgrown()
countcrops = AgCensusViz.countcrops(area)
diversity, cropacres = AgCensusViz.cropdiversity(area)
colnames = ["CropCount", "Entropy", "CropLand"]
df = AgCensusViz.dictstodataframe(colnames, countcrops, diversity, cropacres)
df = df.sort("Entropy")
AgCensusViz.plotdiversity(df)
