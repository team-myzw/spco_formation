# spco_formation

### Overview  

場所概念獲得手法のSpatial_Concept_FormationをSIGVerseのシミュレーション環境上で動かせるようにしたもの 
参考：https://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git

### Description

#### Dependencies
* caffe

1. [Ubuntu 14.04にCaffeをインストール(GPU編)](https://qiita.com/TD72/items/bcb243ee02760ea1d8bb)
2. cd ~/caffe/models/bvlc_reference_caffenet
3. wget http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel
4. cd ~/caffe/data/ilsvrc12
5. sh get_ilsvrc_aux.sh


#### Files

* `/launch/em_navigation.launch` : ナビゲーションを行うlaunch 
* `/launch/em_spco_formation.launch` : データの収集を行うlaunch 

* `/src/em_name2place.py` : 場所の名前から座標の推定を行う（ROS） 
* `/src/name2place.py` : 場所の名前から座標の推定を行う（端末から） 
* `/src/em_place2name.py` : 座標から場所の名前の推定を行う（ROS） 
* `/src/place2name.py` : 座標から場所の名前の推定を行う 
* `/src/Feature_vector_generator.py` : 画像特徴量を求める 

#### Training

1. `__init__.py`のトピック名をデータセットに合わせる。`TRIALNAME`は保存したいデータセットの名前を設定 
2. rosbag2data(1/2) `roslaunch spco_formation em_spco_formation.launch`
3. rosbag2data(2/2) `rosbag play -r 5 exp.bag`
4. 画像特徴量の計算 `python Feature_vector_generator.py ../data/trial`
6. 場所概念学習パラメータ編集(1/2) `gedit ../data/Environment_parameter.txt`
6. 場所概念学習パラメータ編集(2/2) `gedit ../data/space_name.txt`
6. 場所概念学習 `python gibbs_sampling_2016_10.6.py ../data/trial trial/`

学習済データはspco_formationディレクトリ直下に保存されます．  
画像特徴量は`Feature_vector_generator.py`によって生成できます．  
場所概念学習のプログラムの詳細な実行はhttps://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git

#### Navigation

1. `roslaunch spco_formation em_navigation.launch` 
2. `python em_name2place.py <<TRIALNAME>>` 
3. `/spco/name_sub`に移動したい場所の名前を送る 

#### estimate place name

1. `python em_place2name.py <<TRIALNAME>>` 
2. `/spco/place_sub`に場所の座標を送る

#### visualize
* `cd spco_formation/notebooks/spco_visualize.ipynb`