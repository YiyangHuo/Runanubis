1. 安装python 2.7.16 (只要是python2.7版本并且有script文件夹的理论上就可以)  。

2. 在环境变量中添加 安装的好的python27的根目录以及根目录下的 “Scripts” 文件夹。
3. 将根目录下的“python.exe” 拷贝副本 并重命名为 “python2.exe”。 同理，将“Scripts”文件夹下的 "pip.exe" 拷贝副本并重命名为 “pip2.exe” 这么做是为了将python2 与python3 分开，在我的程序里也是直接调用的python2. 所以这一步是必须的。
4. 将本仓库内“anubisplot windows enviroment setup\third party libraries” 文件夹下的matplotlib与mumpy的whl文件放入 “pip2.exe” 所在的Scripts文件夹内。
5. 在cmd中输入 “pip2 install [numpy的whl文件的路径]”。
6. 安装完成后cmd输入 ”python2“ 然后再输入 “ import numpy” 如果没有报错就成功了
7. 安装matplotlib与安装numpy是同理的，注意，安装顺序理应是“numpy” -> “matplotlib”。因为后者是依赖于前者的
8. 环境配置完成