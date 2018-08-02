# spco_formation

### Overview  

場所概念獲得手法のSpatial_Concept_FormationをSIGVerseのシミュレーション環境上で動かせるようにしたもの 
参考：https://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git

### Description

[comingsoon]

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

1. rosbag2data(1/3)`__init__.py`のトピック名をデータセットに合わせる。`TRIALNAME`は保存したいデータセットの名前を設定 
2. rosbag2data(2/3) `roslaunch em_spco_formation em_spco_formation.launch`
3. rosbag2data(3/3) `rosbag play -r 5 exp.bag`
4. 画像特徴量の計算 `python Feature_vector_generator.py ../data/trial`
5. パラメータコピー(1/4) `cp ../data/Environment_parameter.txt  ../data/trial/Environment_parameter.txt`
6. パラメータコピー(2/4) `cp ../data/space_name.txt ../data/trial/space_name.txt`
7. パラメータ編集(3/4) `gedit ../data/trial/Environment_parameter.txt`
8. パラメータ編集(4/4) `gedit ../data/trial/space_name.txt`
9. 場所概念学習 `python gibbs_sampling_2016_10.6.py ../data/trial trial/`

学習済データはspco_formationディレクトリ直下に保存されます．  
画像特徴量は`Feature_vector_generator.py`によって生成できます．  
場所概念学習のプログラムの詳細な実行はhttps://github.com/EmergentSystemLabStudent/Spatial_Concept_Formation.git

#### Training Parameter
* data/trial/Environment_parameter.txt 学習環境とデータ数
    * Max_x_value_of_map 10
    * Max_y_value_of_map 10
    * Min_x_value_of_map -10
    * Min_y_value_of_map -10
    * Number_of_place 3
    * Initial_data_number 1
    * Last_data_number 275
* data/trial/space_name.txt 場所の名前
* parameter/gibbs_hyper_parameter.txt
    * Hyper parameters for Gibss sampling which estimate Place concept. Each parameters are based on graphical model.
    * 5.0 #alfa_0:Parameter of Dirichlet distribution for image features.
    * 0.03 #kappa_0:Parameter of Gaussian distribution for the robot position.
    * 15 #nu_0:Parameter of Gaussian distribution for the robot position.
    * 10000000 #gamma:Parameter of Dirichlet distribution for the class index.
    * 0.01 #beta:Parameter of Dirichlet distribution for words.

* src/gibbs_sampling_2016_10.6.py
    * Stick_large_L=100
    * sigma_init = 100.0 #initial covariance value
    * iteration = 50 #iteration num
#### Navigation

1. `roslaunch spco_formation em_navigation.launch` 
2. `python em_name2place.py <<TRIALNAME>>` 
3. `/spco/name_sub`に移動したい場所の名前を送る 

#### estimate place name

1. `python em_place2name.py <<TRIALNAME>>` 
2. `/spco/place_sub`に場所の座標を送る

#### visualize
* `spco_formation/notebooks/spco_visualize.ipynb`