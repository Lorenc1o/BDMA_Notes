INSERT INTO "cities" ("name", geom) VALUES
('Ixelles', ST_GeomFromText('POINT(4.377307 50.828844)', 4326)),
('Anderlecht', ST_GeomFromText('POINT(4.311476 50.838283)', 4326)),
('Jette', ST_GeomFromText('POINT(4.336345 50.882989)', 4326)),
('Uccle', ST_GeomFromText('POINT(4.372532 50.796875)', 4326)),
('Sint-Pieters-Woluwe', ST_GeomFromText('POINT(4.434936 50.838888)', 4326)),
('Watermaal-Bosvoorde', ST_GeomFromText('POINT(4.418119 50.799759)', 4326)),
('Zaventem', ST_GeomFromText('POINT(4.474544 50.888983)', 4326));

INSERT INTO regions (name, geom)
VALUES ('Brussel-Hoofstad',
ST_GeomFromText('MULTIPOLYGON(((4.479645 50.822743,4.457515
50.820229,4.456853 50.817054,4.45187 50.813328,4.45194
50.811219,4.457141 50.812188,4.460937 50.813218,4.458989
50.810348,4.456116 50.808439,4.486724 50.797359,4.475172
50.791591,4.454373 50.783902,4.439379 50.778243,4.435901
50.779246,4.421607 50.775625,4.416667 50.774577,4.402251
50.77087,4.387639 50.765453,4.387318 50.767396,4.384095
50.772136,4.383319 50.772448,4.375609 50.774116,4.364969
50.775656,4.35601 50.776492,4.347556 50.777496,4.338407
50.776461,4.333619 50.778414,4.329975 50.780467,4.324307
50.789305,4.322575 50.79504,4.317525 50.800722,4.309047
50.802291,4.308363 50.803579,4.308465 50.804311,4.30964
50.80717,4.311257 50.811984,4.311522 50.815316,4.307527
50.816388,4.303343 50.815591,4.301754 50.813618,4.301211
50.810931,4.294128 50.809113,4.289011 50.809436,4.285491
50.811489,4.282386 50.812657,4.277631 50.813553,4.268556
50.813893,4.265531 50.816359,4.263138 50.818998,4.256857
50.819707,4.254612 50.82178,4.250028 50.821461,4.251942
50.824982,4.256682 50.828063,4.259648 50.830789,4.260635
50.835269,4.262463 50.837653,4.268154 50.839206,4.275046
50.839319,4.277955 50.840096,4.288646 50.841081,4.290085
50.843701,4.291939 50.845435,4.291858 50.847707,4.290091
50.850681,4.292963 50.852513,4.292229 50.855179,4.291524
50.857034,4.294124 50.859349,4.286354 50.862307,4.284119
50.867627,4.285793 50.870819,4.294436 50.875666,4.299716
50.878105,4.305949 50.882506,4.307293 50.884232,4.305059
50.885981,4.303219 50.887413,4.301968 50.890233,4.302662
50.892273,4.307749 50.893004,4.319537 50.89579,4.324096
50.896998,4.330009 50.899689,4.337384 50.904432,4.341859
50.904421,4.352447 50.905075,4.365646 50.904144,4.378209
50.903121,4.383628 50.901663,4.387152 50.903259,4.390386
50.909639,4.393336 50.913093,4.400666 50.91564,4.41137
50.916696,4.417836 50.914521,4.417774 50.912572,4.420493
50.911558,4.42832 50.906887,4.428396 50.904615,4.430256
50.902533,4.431213 50.90068,4.435338 50.895791,4.431019
50.891181,4.439619 50.882381,4.434035 50.881243,4.431428
50.878931,4.429613 50.875901,4.42742 50.868888,4.430542
50.863415,4.434736 50.864046,4.43563 50.86406,4.439634
50.862739,4.44479 50.861355,4.448267 50.860514,4.451311
50.857312,4.460166 50.856063,4.464033 50.854983,4.465028
50.851913,4.469804 50.846463,4.471775 50.844788,4.471915
50.840488,4.470134 50.836404,4.475079 50.829658,4.479645
50.822743)))', 4326));