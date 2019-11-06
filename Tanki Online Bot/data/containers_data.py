import random
import numpy

item_list = {"a common":{"3,500 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 3500, "xp": 50},
                         "125 Double Armor":{"image": "https://i.imgur.com/HfrwpgC.png", "att": 125, "xp": 50},
                         "125 Double Damage":{"image": "https://i.imgur.com/FWXPzIR.png", "att": 125, "xp": 50},
                         "125 Speed Boost":{"image": "https://i.imgur.com/prSNowH.png", "att": 125, "xp": 50},
                         "125 Mine":{"image": "https://i.imgur.com/RAahEO7.png", "att": 125, "xp": 50}}, #Finished

             "an uncommon":{"10,000 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 10000, "xp": 100},
                            "125 Repair Kits":{"image": "https://i.imgur.com/SY2qjiW.png", "att": 125, "xp": 100},
                            "50 Batteries":{"image": "https://i.imgur.com/E8Nw5Bq.png", "att": 50, "xp": 100},
                            "100 of all Supplies":{"image": "https://i.imgur.com/wTvTgWn.png", "att": 50, "xp": 100},
                            #"3 days of Premium Account":{"image": "https://i.imgur.com/lgDo2Eu.png", "att": 3500, "xp": 100},
                            "5 Gold Boxes":{"image": "https://i.imgur.com/2BAGUnn.png", "att": 3500, "xp": 100}},#Finished

             "a rare":{"25,000 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 25000, "xp": 150},
                       "150 Batteries":{"image": "https://i.imgur.com/E8Nw5Bq.png", "att": 150, "xp": 150},
                       "250 of all Supplies":{"image": "https://i.imgur.com/pokkXpZ.png", "att": 50, "xp": 150}, #Fix Supplies image
                       #"10 days of Premium Account":{"image": "https://i.imgur.com/lgDo2Eu.png", "att": 3500, "xp": 150},
                       "10 Gold Boxes":{"image": "https://i.imgur.com/2BAGUnn.png", "att": 10, "xp": 150}}, #Garage Paint added, Football Paints added

             "an epic":{"100,000 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 100000, "xp": 250},
             "100 Red Crystals":{"image": "https://i.imgur.com/pv10bs8.png", "att": 100, "xp": 250}}, #Shop Paint added, Legendary non-animated Paint added,Premium Paints added

             "a legendary":{"300,000 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 300000, "xp": 350},
             "250 Red Crystals":{"image": "https://i.imgur.com/pv10bs8.png", "att": 250, "xp": 350}}, #Animated Paints

             "an exotic":{"1,000,000 Crystals":{"image": "https://i.imgur.com/iDkbkht.png", "att": 1000000, "xp": 500},
                        "Firebird <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/JLTDQEu.png", "att": 1, "xp": 500},
                        "Vulcan <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/YAPFGLS.png", "att": 1, "xp": 500},
                        "Thunder <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/jn7HXPn.png", "att": 1, "xp": 500},#500,000<=======================================
                        "Railgun <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/6qTc1Hq.png", "att": 1, "xp": 500},
                        "Wasp <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/48UOa4U.png", "att": 1, "xp": 500},
                        "Hornet <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/fYAI4HT.png", "att": 1, "xp": 500},
                        "Ricochet <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/6jt9MQC.png", "att": 1, "xp": 500},
                        "Viking <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/7pH1zld.png", "att": 1, "xp": 500},
                        "Mammoth <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/MsSu9WG.png", "att": 1, "xp": 500}, #XT Skins
                        "Titan <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/iU6PKwx.png", "att": 1, "xp": 500}, #XT Skins
                        "Smoky <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/TRWVjfa.png", "att": 1, "xp": 500}, #XT Skins
                        "Freeze <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/9OFRNqV.png", "att": 1, "xp": 500}, #XT Skins
                        "Isida <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/xO6u36X.png", "att": 1, "xp": 500}, #XT Skins
                        "Twins <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/mjUw7Bu.png", "att": 1, "xp": 500}, #XT Skins
                        "Dictator <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/NHzOfH4.png", "att": 1, "xp": 500}, #XT Skins
                        "Shaft <:Icon_XT_skin:545734382682636288>":{"image": "https://i.imgur.com/7PDMj18.png", "att": 1, "xp": 500},
                        "500 Red Crystals":{"image": "https://i.imgur.com/pv10bs8.png", "att": 500, "xp": 500}}} #XT Skins
#rare
garage_paints1 = {"Lava":{"image": "https://i.imgur.com/XCZbZRM.png", "att": 1, "xp": 150},
                "Lead":{"image": "https://i.imgur.com/uhhtrj5.png", "att": 1, "xp": 150},
                "Invader":{"image": "https://i.imgur.com/g1wNZhb.png", "att": 1, "xp": 150},
                "Safari":{"image": "https://i.imgur.com/vYPz9P1.png", "att": 1, "xp": 150},
                "Dragon":{"image": "https://i.imgur.com/5mjWl9h.png", "att": 1, "xp": 150},
                "Magma":{"image": "https://i.imgur.com/diE3IEZ.png", "att": 1, "xp": 150},
                "Mary":{"image": "https://i.imgur.com/ACP8f0O.png", "att": 1, "xp": 150},
                "Sahara":{"image": "https://i.imgur.com/ohyd10B.png", "att": 1, "xp": 150},
                "Night":{"image": "https://i.imgur.com/eHdsCQh.png", "att": 1, "xp": 150},
                "Storm":{"image": "https://i.imgur.com/7pJNDtb.png", "att": 1, "xp": 150},
                "In Love":{"image": "https://i.imgur.com/1StT6Rv.png", "att": 1, "xp": 150},
                "Carbon":{"image": "https://i.imgur.com/F28G5O8.png", "att": 1, "xp": 150},
                "Confetti":{"image": "https://i.imgur.com/QZssxkB.png", "att": 1, "xp": 150},
                "Alien":{"image": "https://i.imgur.com/H5Kz1U6.png", "att": 1, "xp": 150},
                "Chainmail":{"image": "https://i.imgur.com/3VRjXpK.png", "att": 1, "xp": 150},
                "Dirty":{"image": "https://i.imgur.com/IOOuqCH.png", "att": 1, "xp": 150},
                "Jaguar":{"image": "https://i.imgur.com/RnsVNXK.png", "att": 1, "xp": 150},
                "Desert":{"image": "https://i.imgur.com/lp08Z29.png", "att": 1, "xp": 150},
                "Guerrilla":{"image": "https://i.imgur.com/FE89UwD.png", "att": 1, "xp": 150},
                "Swash":{"image": "https://i.imgur.com/cBPqSLL.png", "att": 1, "xp": 150},
                "Harlequin":{"image": "https://i.imgur.com/5Brxb1F.png", "att": 1, "xp": 150},
                "Pixel":{"image": "https://i.imgur.com/ilKtSGl.png", "att": 1, "xp": 150},
                "Corrosion":{"image": "https://i.imgur.com/bwlBlRA.png", "att": 1, "xp": 150},
                "Tundra":{"image": "https://i.imgur.com/c577Vfe.png", "att": 1, "xp": 150},
                "Vortex":{"image": "https://i.imgur.com/x6pH3Vc.png", "att": 1, "xp": 150},
                "Pixel Heart":{"image": "https://i.imgur.com/ph0pFnw.png", "att": 1, "xp": 150},
                "Roger":{"image": "https://i.imgur.com/R7xwfPe.png", "att": 1, "xp": 150},
                "Fracture":{"image": "https://i.imgur.com/Vf4Eyuy.png", "att": 1, "xp": 150},
                "Cedar":{"image": "https://i.imgur.com/cKLpfvz.png", "att": 1, "xp": 150},
                "Python":{"image": "https://i.imgur.com/nXS8LJt.png", "att": 1, "xp": 150},
                "Sakura":{"image": "https://i.imgur.com/nLH8BbC.png", "att": 1, "xp": 150},
                "Grasslands":{"image": "https://i.imgur.com/NZfwM1J.png", "att": 1, "xp": 150},
                "Soft Flowers":{"image": "https://i.imgur.com/rog1IO4.png", "att": 1, "xp": 150},
                "Electra":{"image": "https://i.imgur.com/2Kc6byT.png", "att": 1, "xp": 150},
                "Moss":{"image": "https://i.imgur.com/RVI3QOW.png", "att": 1, "xp": 150},
                "First Love":{"image": "https://i.imgur.com/ku6VMEj.png", "att": 1, "xp": 150},
                "Sandstone":{"image": "https://i.imgur.com/AVMJk2X.png", "att": 1, "xp": 150},
                "Spark":{"image": "https://i.imgur.com/kRKh6Jz.png", "att": 1, "xp": 150},
                "Jeans":{"image": "https://i.imgur.com/HfU9OeD.png", "att": 1, "xp": 150},
                "Digital":{"image": "https://i.imgur.com/gNsQabm.png", "att": 1, "xp": 150},
                "Rustle":{"image": "https://i.imgur.com/MnRmLDS.png", "att": 1, "xp": 150},
                "Blacksmith":{"image": "https://i.imgur.com/20zUryA.png", "att": 1, "xp": 150},
                "Hohloma":{"image": "https://i.imgur.com/KwqwX21.png", "att": 1, "xp": 150},
                "Loam":{"image": "https://i.imgur.com/XB93uMr.png", "att": 1, "xp": 150},
                "Rhino":{"image": "https://i.imgur.com/FmQDirF.png", "att": 1, "xp": 150},
                "Winter":{"image": "https://i.imgur.com/2vzj6f7.png", "att": 1, "xp": 150},
                "Urban":{"image": "https://i.imgur.com/pq7viBm.png", "att": 1, "xp": 150},
                "Sweater":{"image": "https://i.imgur.com/HeXiVOR.png", "att": 1, "xp": 150},
                "Atom":{"image": "https://i.imgur.com/hRVV21d.png", "att": 1, "xp": 150},
                "Savanna":{"image": "https://i.imgur.com/meAmmWc.png", "att": 1, "xp": 150},
                "Cherry":{"image": "https://i.imgur.com/UzTeI3s.png", "att": 1, "xp": 150},
                "Emerald":{"image": "https://i.imgur.com/fywAfNU.png", "att": 1, "xp": 150},
                "Irbis":{"image": "https://i.imgur.com/xfVl0H2.png", "att": 1, "xp": 150},
                "Disco":{"image": "https://i.imgur.com/VuUbOHO.png", "att": 1, "xp": 150},
                "Mars":{"image": "https://i.imgur.com/zi5sCbk.png", "att": 1, "xp": 150},
                "Hive":{"image": "https://i.imgur.com/uLTSr7x.png", "att": 1, "xp": 150},
                "Inferno":{"image": "https://i.imgur.com/zfllNNC.png", "att": 1, "xp": 150},
                "Jade":{"image": "https://i.imgur.com/eNIu0iM.png", "att": 1, "xp": 150},
                "Tiger":{"image": "https://i.imgur.com/hLMY8KU.png", "att": 1, "xp": 150},
                "Kaleidoscope":{"image": "https://i.imgur.com/p3NllDC.png", "att": 1, "xp": 150},
                "Taiga":{"image": "https://i.imgur.com/jkD2fZ0.png", "att": 1, "xp": 150},
                "Red Urban":{"image": "https://i.imgur.com/wIzOQ8v.png", "att": 1, "xp": 150},
                "Nano":{"image": "https://i.imgur.com/I2k64fR.png", "att": 1, "xp": 150},
                "Prodigi":{"image": "https://i.imgur.com/loGcRXM.png", "att": 1, "xp": 150},
                "Rock":{"image": "https://i.imgur.com/D8TXZcJ.png", "att": 1, "xp": 150},
                "Raccon":{"image": "https://i.imgur.com/KTGc1QQ.png", "att": 1, "xp": 150},
                "Needle":{"image": "https://i.imgur.com/iTXtOeR.png", "att": 1, "xp": 150},
                "Picasso":{"image": "https://i.imgur.com/KhQH7A1.png", "att": 1, "xp": 150},
                "Space":{"image": "https://i.imgur.com/qCbJMJ1.png", "att": 1, "xp": 150},
                "Graffiti":{"image": "https://i.imgur.com/079nkmA.png", "att": 1, "xp": 150},
                "Zeus":{"image": "https://i.imgur.com/PADN5LV.png", "att": 1, "xp": 150},
                "Clay":{"image": "https://i.imgur.com/clYBs2a.png", "att": 1, "xp": 150},
                "Lumberjack":{"image": "https://i.imgur.com/e8NoL8V.png", "att": 1, "xp": 150},
                "Africa":{"image": "https://i.imgur.com/ZGUfC1F.png", "att": 1, "xp": 150}}
#rare
footbal_paints1 = {"Australia":{"image": "https://i.imgur.com/iGuVO9O.png", "att": 1, "xp": 150},
                "England":{"image": "https://i.imgur.com/t3eElQx.png", "att": 1, "xp": 150},
                "Argentina":{"image": "https://i.imgur.com/zMgReuu.png", "att": 1, "xp": 150},
                "Belgium":{"image": "https://i.imgur.com/z1K1Fk0.png", "att": 1, "xp": 150},
                "Brazil":{"image": "https://i.imgur.com/3NV1Reg.png", "att": 1, "xp": 150},
                "Denmark":{"image": "https://i.imgur.com/8mqCju3.png", "att": 1, "xp": 150},
                "Germany":{"image": "https://i.imgur.com/q2uEW9d.png", "att": 1, "xp": 150},
                "Egypt":{"image": "https://i.imgur.com/VM09xBx.png", "att": 1, "xp": 150},
                "Iran":{"image": "https://i.imgur.com/fDDaOOA.png", "att": 1, "xp": 150},
                "Iceland":{"image": "https://i.imgur.com/KCr9ftZ.png", "att": 1, "xp": 150},
                "Spain":{"image": "https://i.imgur.com/Ax6pneE.png", "att": 1, "xp": 150},
                "Colombia":{"image": "https://i.imgur.com/tinjQNi.png", "att": 1, "xp": 150},
                "Costa Rica":{"image": "https://i.imgur.com/zanlQCa.png", "att": 1, "xp": 150},
                "Morocco":{"image": "https://i.imgur.com/mA3RLP6.png", "att": 1, "xp": 150},
                "Mexico":{"image": "https://i.imgur.com/PmXv22K.png", "att": 1, "xp": 150},
                "Nigeria":{"image": "https://i.imgur.com/yYpk93Z.png", "att": 1, "xp": 150},
                "Panama":{"image": "https://i.imgur.com/TkJWAGJ.png", "att": 1, "xp": 150},
                "Peru":{"image": "https://i.imgur.com/gV5FKgr.png", "att": 1, "xp": 150},
                "Portugal":{"image": "https://i.imgur.com/zdPfaP1.png", "att": 1, "xp": 150},
                "Poland":{"image": "https://i.imgur.com/TvcgtPM.png", "att": 1, "xp": 150},
                "South Korea":{"image": "https://i.imgur.com/yNcMdZU.png", "att": 1, "xp": 150},
                "Russia":{"image": "https://i.imgur.com/XOM8MAg.png", "att": 1, "xp": 150},
                "Saudi Arabia":{"image": "https://i.imgur.com/UG6Rj8d.png", "att": 1, "xp": 150},
                "Senegal":{"image": "https://i.imgur.com/yYe9cJF.png", "att": 1, "xp": 150},
                "Serbia":{"image": "https://i.imgur.com/aPaDfOE.png", "att": 1, "xp": 150},
                "Tunisia":{"image": "https://i.imgur.com/eQz9uOW.png", "att": 1, "xp": 150},
                "Uruguay":{"image": "https://i.imgur.com/DANrCSF.png", "att": 1, "xp": 150},
                "France":{"image": "https://i.imgur.com/koBUCxc.png", "att": 1, "xp": 150},
                "Croatia":{"image": "https://i.imgur.com/n9M504u.png", "att": 1, "xp": 150},
                "Switzerland":{"image": "https://i.imgur.com/y1KEttR.png", "att": 1, "xp": 150},
                "Sweden":{"image": "https://i.imgur.com/H9d9yyx.png", "att": 1, "xp": 150},
                "Japan":{"image": "https://i.imgur.com/km8gIFH.png", "att": 1, "xp": 150}}
#epic
shop_paints1 = {"Arachnid":{"image": "https://i.imgur.com/1r5ltoM.png", "att": 1, "xp": 250},
                "Liquid Metal":{"image": "https://i.imgur.com/d69BcAK.png", "att": 1, "xp": 250},
                "Drought":{"image": "https://i.imgur.com/ULKjFX8.png", "att": 1, "xp": 250},
                "Strawberry":{"image": "https://i.imgur.com/p1nvp2W.png", "att": 1, "xp": 250},
                "Barber Shop":{"image": "https://i.imgur.com/pn2cR7T.png", "att": 1, "xp": 250},
                "Scandinavia":{"image": "https://i.imgur.com/D0FdUUw.png", "att": 1, "xp": 250},
                "Lunar Soil":{"image": "https://i.imgur.com/CmSfRJk.png", "att": 1, "xp": 250},
                "Rust":{"image": "https://i.imgur.com/x4o7JRi.png", "att": 1, "xp": 250},
                "Steak":{"image": "https://i.imgur.com/aCEwO2t.png", "att": 1, "xp": 250},
                "Amber":{"image": "https://i.imgur.com/nWxmqth.png", "att": 1, "xp": 250},
                "Lime":{"image": "https://i.imgur.com/tBDPCvI.png", "att": 1, "xp": 250},
                "Neuron":{"image": "https://i.imgur.com/iaI4p5Z.png", "att": 1, "xp": 250},
                "Domino":{"image": "https://i.imgur.com/SaouxYq.png", "att": 1, "xp": 250},
                "Mint":{"image": "https://i.imgur.com/8Vqm0Ia.png", "att": 1, "xp": 250},
                "Watercolor":{"image": "https://i.imgur.com/0Slef4O.png", "att": 1, "xp": 250},
                "Pajamas":{"image": "https://i.imgur.com/nWvmphL.png", "att": 1, "xp": 250},
                "Vanadium":{"image": "https://i.imgur.com/AxDdDEP.png", "att": 1, "xp": 250},
                "Glitch":{"image": "https://i.imgur.com/elYaNB5.png", "att": 1, "xp": 250},
                "Sunset Camouflage":{"image": "https://i.imgur.com/JnX8DrT.png", "att": 1, "xp": 250},
                "All You Need Is":{"image": "https://i.imgur.com/XoW4Xhe.png", "att": 1, "xp": 250},
                "Zombie":{"image": "https://i.imgur.com/23kEACB.png", "att": 1, "xp": 250},
                "Fire of Valor":{"image": "https://i.imgur.com/MZDnyFJ.png", "att": 1, "xp": 250},
                "Spangles":{"image": "https://i.imgur.com/3k1vYLp.png", "att": 1, "xp": 250},
                "Snowflake":{"image": "https://i.imgur.com/onfbAeU.png", "att": 1, "xp": 250},
                "Lilac Petals":{"image": "https://i.imgur.com/UDXnwo0.png", "att": 1, "xp": 250},
                "Retina":{"image": "https://i.imgur.com/6cWWaX0.png", "att": 1, "xp": 250},
                "Chill bro!":{"image": "https://i.imgur.com/4aZQkOo.png", "att": 1, "xp": 250},
                "Secret of the Aliens":{"image": "https://i.imgur.com/7sGpwkp.png", "att": 1, "xp": 250},
                "New Year 2018":{"image": "https://i.imgur.com/vxZluMV.png", "att": 1, "xp": 250},
                "Azure":{"image": "https://i.imgur.com/RjlfYZn.png", "att": 1, "xp": 250},
                "Gucciflage":{"image": "https://i.imgur.com/17Zg17F.png", "att": 1, "xp": 250},
                "Hallucination":{"image": "https://i.imgur.com/bMYUqrw.png", "att": 1, "xp": 250},
                "Hypercube":{"image": "https://i.imgur.com/Ovss4Hd.png", "att": 1, "xp": 250},
                "Kungur Ice Cave":{"image": "https://i.imgur.com/vXSGSb9.png", "att": 1, "xp": 250},
                "Lollipop":{"image": "https://i.imgur.com/tjpfb7h.png", "att": 1, "xp": 250},
                "Lotus":{"image": "https://i.imgur.com/NpDp2SW.png", "att": 1, "xp": 250},
                "Monet":{"image": "https://i.imgur.com/wmFBrqf.png", "att": 1, "xp": 250},
                "Paisley Flame":{"image": "https://i.imgur.com/pHV1BWP.png", "att": 1, "xp": 250},
                "Paisley Ice":{"image": "https://i.imgur.com/GBS8Oei.png", "att": 1, "xp": 250},
                "Peaks":{"image": "https://i.imgur.com/uCgQgoC.png", "att": 1, "xp": 250},
                "Phantom":{"image": "https://i.imgur.com/rBPaqZL.png", "att": 1, "xp": 250},
                "Play-Doh":{"image": "https://i.imgur.com/jMIKwqu.png", "att": 1, "xp": 250},
                "Pop Art":{"image": "https://i.imgur.com/oZYpvEp.png", "att": 1, "xp": 250},
                "Potter":{"image": "https://i.imgur.com/eVzsHfx.png", "att": 1, "xp": 250},
                "Pulsar":{"image": "https://i.imgur.com/454HkW6.png", "att": 1, "xp": 250},
                "Ripple":{"image": "https://i.imgur.com/z8E4UHX.png", "att": 1, "xp": 250},
                "Sillicate":{"image": "https://i.imgur.com/tURQLHs.png", "att": 1, "xp": 250},
                "Sudoku":{"image": "https://i.imgur.com/N1u6qGC.png", "att": 1, "xp": 250},
                "Zigzag":{"image": "https://i.imgur.com/76q5osN.png", "att": 1, "xp": 250},
                "Abstract Lines":{"image": "https://i.imgur.com/iqokg3G.png", "att": 1, "xp": 250},
                "Blue Square":{"image": "https://i.imgur.com/K9A0kj8.png", "att": 1, "xp": 250},
                "Condensed Milk":{"image": "https://i.imgur.com/SQxZwmr.png", "att": 1, "xp": 250},
                "E236":{"image": "https://i.imgur.com/8H1shmx.png", "att": 1, "xp": 250},
                "Feathers":{"image": "https://i.imgur.com/hPGozkE.png", "att": 1, "xp": 250},
                "Fire Dragon":{"image": "https://i.imgur.com/Q3OosIa.png", "att": 1, "xp": 250},
                "Megapolis":{"image": "https://i.imgur.com/Behihq4.png", "att": 1, "xp": 250},
                "Stained Glass":{"image": "https://i.imgur.com/Z2KJzvo.png", "att": 1, "xp": 250},
                "Thunderball":{"image": "https://i.imgur.com/8FBsH3U.png", "att": 1, "xp": 250}}
#epic
legendary_paints_no_anim1 = {"Moonwalker":{"image": "https://i.imgur.com/JUrnzRT.png", "att": 1, "xp": 250},
                            "Eternity":{"image": "https://i.imgur.com/UMAh7sd.png", "att": 1, "xp": 250},
                            "Red Suit":{"image": "https://i.imgur.com/03GIdFr.png", "att": 1, "xp": 250},
                            "Golden Star":{"image": "https://i.imgur.com/e6QtzC1.png", "att": 1, "xp": 250},
                            "Frost":{"image": "https://i.imgur.com/hFwjkAR.png", "att": 1, "xp": 250}}
#legendary
premium_paint1 = {"Flow":{"image": "https://i.imgur.com/4qPgNUD.png", "att": 1, "xp": 350},
                "Nightmare":{"image": "https://i.imgur.com/1VBt3aN.png", "att": 1, "xp": 350},
                "Spectrum":{"image": "https://i.imgur.com/dh32bzz.png", "att": 1, "xp": 350},
                "Holiday Lights":{"image": "https://i.imgur.com/52dZq7G.png", "att": 1, "xp": 350},
                "Matrix":{"image": "https://i.imgur.com/BDJE2Tc.png", "att": 1, "xp": 350},
                "Mosaic":{"image": "https://i.imgur.com/LAGopve.png", "att": 1, "xp": 350},
                "Vertigo":{"image": "https://i.imgur.com/I0j0GcM.png", "att": 1, "xp": 350},
                "Prodigy 2.0":{"image": "https://i.imgur.com/1ERmkig.png", "att": 1, "xp": 350},
                "War. The Winner":{"image": "https://i.imgur.com/EEmBWRf.png", "att": 1, "xp": 350},
                "Ginga":{"image": "https://i.imgur.com/z5E8sDE.png", "att": 1, "xp": 350},
                "Magnolia":{"image": "https://i.imgur.com/z5E8sDE.png", "att": 1, "xp": 350},
                "Galaxy":{"image": "https://i.imgur.com/54e6M7y.png", "att": 1, "xp": 350},
                "Eruption":{"image": "https://i.imgur.com/vrc883L.png", "att": 1, "xp": 350},
                "Siberian Tiger":{"image": "https://i.imgur.com/7itsTVG.png", "att": 1, "xp": 350},
                "Secret Sauce":{"image": "https://i.imgur.com/230vVbB.png", "att": 1, "xp": 350},
                "Canyon Hero":{"image": "https://i.imgur.com/io1bK4Q.png", "att": 1, "xp": 350},
                "Pastila":{"image": "https://i.imgur.com/SgCg1fq.png", "att": 1, "xp": 350},
                "Prestigio":{"image": "https://i.imgur.com/yab24Fs.png", "att": 1, "xp": 350},
                "Valour":{"image": "https://i.imgur.com/XcZpg4t.png", "att": 1, "xp": 350},
                "Beholder":{"image": "https://i.imgur.com/qlZ9J0e.png", "att": 1, "xp": 350},
                "Synesthesia":{"image": "https://i.imgur.com/YEhLbRl.png", "att": 1, "xp": 350},
                "Gears":{"image": "https://i.imgur.com/4RcHdnJ.png", "att": 1, "xp": 350},
                "Radioactive Jelly":{"image": "https://i.imgur.com/KHpjspf.png", "att": 1, "xp": 350},
                "Spinner":{"image": "https://i.imgur.com/gPzFkAM.png", "att": 1, "xp": 350},
                "Tentacles":{"image": "https://i.imgur.com/DaUMELL.png", "att": 1, "xp": 350},
                "LEDs":{"image": "https://i.imgur.com/0Rlydtn.png", "att": 1, "xp": 350},
                "Meteor Shower":{"image": "https://i.imgur.com/ynclPod.png", "att": 1, "xp": 350},
                "Fall Leaves": {"image": "https://i.imgur.com/N8xbd6S.png", "att": 1, "xp": 350},
                "Electrohive": {"image": "https://i.imgur.com/eBMVxEC.png", "att": 1, "xp": 350},
                "Synth-pop": {"image": "https://i.imgur.com/j9DEseF.png", "att": 1, "xp": 350},
                "Runes": {"image": "https://i.imgur.com/uznlaGH.png", "att": 1, "xp": 350},
                "Symbiote": {"image": "https://i.imgur.com/u9H9fE2.png", "att": 1, "xp": 350},
                "Tic-tac-toe": {"image": "https://i.imgur.com/x2YtYp6.png", "att": 1, "xp": 350},
                "Barbed Wire": {"image": "https://i.imgur.com/ByGXpin.png", "att": 1, "xp": 350},
                "Bunny": {"image": "https://i.imgur.com/rFrn58g.png", "att": 1, "xp": 350},
                "Touch of chill": {"image": "https://i.imgur.com/FnUMKc3.png", "att": 1, "xp": 350}}










def containeradd():
    garage_paints = random.choice(list(garage_paints1.items()))
    gtext = garage_paints[0]
    gnumber = garage_paints[1]
    item_list['a rare'][gtext] = gnumber

    footbal_paints = random.choice(list(footbal_paints1.items()))
    ftext = footbal_paints[0]
    fnumber = footbal_paints[1]
    item_list['a rare'][ftext] = fnumber

    shop_paints = random.choice(list(shop_paints1.items()))
    stext = shop_paints[0]
    snumber = shop_paints[1]
    item_list['an epic'][stext] = snumber

    legendary_paints_no_anim = random.choice(list(legendary_paints_no_anim1.items()))
    ltext = legendary_paints_no_anim[0]
    lnumber = legendary_paints_no_anim[1]
    item_list['an epic'][ltext] = lnumber

    premium_paint = random.choice(list(premium_paint1.items()))
    ptext = premium_paint[0]
    pnumber = premium_paint[1]
    item_list['a legendary'][ptext] = pnumber




colors = {"a common": 0xd3d3d3, "an uncommon":0x32cd32, "a rare":0x05c8ff, "an epic":0x9400d3, "a legendary":0xf4f142, "an exotic":0xd8261a}
