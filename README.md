# spco_formation

### Overview  

場所概念獲得手法のSpatial_Concept_FormationをSIGVerseのシミュレーション環境上で動かせるようにしたもの 
参考：https://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git

### Description

###### Files

* `/launch/em_navigation.launch` : ナビゲーションを行うlaunch 
* `/launch/em_spco_formation.launch` : データの収集を行うlaunch 

* `/src/em_name2place.py` : 場所の名前から座標の推定を行う（ROS） 
* `/src/name2place.py` : 場所の名前から座標の推定を行う（端末から） 
* `/src/em_place2name.py` : 座標から場所の名前の推定を行う（ROS） 
* `/src/place2name.py` : 座標から場所の名前の推定を行う 
* `/src/Feature_vector_generator.py` : 画像特徴量を求める 

###### Training

1. `__init__.py`のトピック名をデータセットに合わせる 
2. `roslaunch spco_formation em_spco_formation.launch`

学習済データはspco_formationディレクトリ直下に保存されます．  
画像特徴量は`Feature_vector_generator.py`によって生成できます．  
場所概念学習のプログラムの実行はhttps://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git と同様です．

###### Navigation

1. `roslaunch spco_formation em_navigation.launch` 
2. `python em_name2place.py` 
3. `/spco/name_sub`に移動したい場所の名前を送る 

###### estimate place name

1. `python em_place2name.py` 
2. `/spco/place_sub`に場所の座標を送る
