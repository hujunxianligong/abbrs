# 使用说明 
 
该代码版本主要是做训练集生成以及加载模型运行接口调用，模型的训练部分请自行参考CRF++训练模型

## python环境
请使用python3.0+环境进行操作
## pip安装包
```bash
$ apt-get install libvirt-dev
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade pip
$ sudo pip3 install -r requirements.txt

```

## make编译安装
*  下载地址： https://taku910.github.io/crfpp/
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
````
安装以下依赖
$ sudo apt-get install python3-dev
````
依赖软链接
```
$ sudo ln -s /usr/local/lib/libcrfpp.so.0 /usr/lib/
```

如果出现以下错误
```
ImportError:/home/×××/anaconda2/bin/.../libstdc++.so.6: versionGLIBCXX_3.4.XX’ not found`

```
请更新更新libgcc

hanlp配置修改，请进入pyhanlp依赖目录下中替换`hanlp.properties`
```
/home/{$user}/.pyenv/versions/3.4.3/envs/env343/lib/python3.4/site-packages/pyhanlp/static
```
路径可能略有差别。

## 运行注意


* 配置文件设置
`config.py`和`config_debug.py`
词典路径，训练集输出路径和模型路径必须设置

* 训练集生成
```
在train/corpus_tran_train.py方法里面调用方法
pt = Pretreatment()
pt.get_train_pretreatment(None,{$companyNamePathFile})
```

* 访问接口
```
$curl -d "华为技术有限公司" http://localhost:5007/api/abbner
```

* 目录有接口启动脚本使用bash 启动即可
```
$ mkdir log
$ ./start.sh
```