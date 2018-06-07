# abbrs
基于双层条件随机场的中文公司名简称生成
* Flask架构，提供高可用的API服务
* Argparse设计，便于命令操作
* 基于HMM的前向后向算法构建有向概率图
* 基于维特比算法构建的解析求解最大概率解
* 完整流程，从语料到训练集至模型生成 
* 更多特性等你发现……


# 组件介绍
分为两层处理，分类（classify）与切分（seg）。

## classify
将公司名基于自定义类型做分类，为之后简称缩略模型提供支持以及规则模型提供支持

## seg
利用classify结果结合其他特征来获取最终简称集合

# 目录介绍
* project
    * bin  //中间交换结构   
    * doc 
    * load  //加载模型
    * preprocessor  //预处理语语料
    * train  //训练模型
    * util  //工具 <br>
  app.py  //API入口 <br>
  config.py  //配置 <br>


# 环境准备 
 
## python环境
请使用python3环境进行操作
### pip安装包
```bash
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade pip
$ sudo pip3 install -r requirements.txt

```

### make编译安装
*  下载地址： https://taku910.github.io/crfpp/
下载CRF++-0.58.tar.gz
解压完毕后，进入软件主目录
```
$ ./configure
$ make
$ sudo make install
```
至此已经编译好了，下一步安装python接口。进入子目录python中
```
$ cd python
$ python3 setup.py build
$ sudo python3 setup.py install
```

如果出现
```
error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```

安装以下依赖
```
$ sudo apt-get install python3-dev
```

依赖软链接
```
$ sudo ln -s /usr/local/lib/libcrfpp.so.0 /usr/lib/
```

如果出现以下错误
```
ImportError:/home/×××/anaconda2/bin/.../libstdc++.so.6: versionGLIBCXX_3.4.XX’ not found`

```
请更新libgcc

hanlp配置修改，请下载hanlp的自定义词典并解压并且在`cmb_abbr`目录下的`generate_stage/jar/hanlp.properties`配置对应的绝对路径
```
/home/{$user}/.pyenv/versions/3.4.3/envs/env343/lib/python3.4/site-packages/pyhanlp/static
```
路径可能略有差别。

### 运行注意


* 配置文件设置
`config.py`和`config_debug.py`
词典路径，训练集输出路径和模型路径必须设置

* 训练集生成
```
在train/corpus_tran_train.py方法里面调用方法.
假如有一个公司名文件调用下面的函数传入文件名路径即可再配置文件的输出路径得到结果
pt = Pretreatment()
pt.get_train_pretreatment(None,{$companyNamePathFile})
```

* 模型训练
<br>在已经安装完成CRF++ 环境下使用命令行对训练集进行训练<br>
```
$ crf_learn -c 1 -f 1 template {$训练集路径} {$输出模型文件路径}
```
[N]:template是训练时生成特征函数的特征模板，根据自身需求制定。
目前使用的分类模板如下:
```txt
# Unigram
U00:%x[-2,0]
U01:%x[-1,0]
U02:%x[0,0]
U03:%x[1,0]
U04:%x[2,0]
U05:%x[-1,0]/%x[0,0]
U06:%x[0,0]/%x[1,0]
U07:%x[1,0]/%x[2,0]
U08:%x[-2,0]/%x[-1,0]

* 结果说明
1、简称中不会出现全称
2、简称最多5个
3、简称位置靠前的准确度越高

# Bigram
B
```
* API启动
<br>目录有接口启动脚本使用bash 启动即可
```
$ ./start.sh
```
* 访问接口
```
$ curl -d "华为技术有限公司" http://localhost:5007/api/abbner
```

