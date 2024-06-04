film = {"Items":[{"Name":"The Bourne Supremacy","ServerId":"17cb60feb69343e98d5fe8bfa895f98f","Id":"7c7d46474c1688061508cafad438a500","HasSubtitles":True,"Container":"mkv","PremiereDate":"2004-07-23T00:00:00.0000000Z","CriticRating":82,"OfficialRating":"DK-11","CommunityRating":7.321,"RunTimeTicks":65115050000,"ProductionYear":2004,"IsFolder":False,"Type":"Movie","VideoType":"VideoFile","ImageTags":{"Primary":"aa1ca101ca887a2e07c5e1ad7faa0e96","Logo":"7064ed0d7f95fce2810f2e2830f8c0d5","Thumb":"830f9e206937cb1886fe301256be3772"},"BackdropImageTags":["2d3890fcaf8bbc1f28ffaaaa367b6ef4"],"ImageBlurHashes":{"Backdrop":{"2d3890fcaf8bbc1f28ffaaaa367b6ef4":"W84:AwV?F~t:-mpKv|krDOV?-;VqwakDozemtSo#MyadxakDIUbI"},"Primary":{"aa1ca101ca887a2e07c5e1ad7faa0e96":"dJCYmixu%0=^o}X89^Ndb]s;NIR*#-NI=ww]0$s.WEIq"},"Logo":{"7064ed0d7f95fce2810f2e2830f8c0d5":"HnODnIofxuWBIUj[t7ofIU~qM{t7ofM{WBt7WBRj"},"Thumb":{"830f9e206937cb1886fe301256be3772":"WQE.al?FxYtMSIxU~Sogt6j?WToI9uNGaenm%1R.E1s*oJog-ot7"}},"LocationType":"FileSystem","MediaType":"Video"}],"TotalRecordCount":1,"StartIndex":0}

# parse the JSON
print(film["Items"])
movie = film["Items"][0]
print("new line")
print(movie['Name'])
