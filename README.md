## 插件功能
1. 解析codecc json文件，获取代码严重、一般、提示问题数量

## 插件打包
 1. 进入插件代码工程根目录下
 2. 执行 python setup.py sdist (或其他打包命令，本示例以sdist为例)
 3. 在任意位置新建文件夹，如 parseCodecc_release
 4. 将步骤 2 生产的执行包拷贝到 parseCodecc_release 下
 5. 添加task.json文件到 parseCodecc_release 下
 6. 把 parseCodecc_release 使用`zip -r parseCodecc.zip parseCodecc_release`打成zip包即可 

## 插件安装
1. 插件名称随便取
2. 插件标识必须为parseCodecc
3. 开发语言为python
4. 自定义前端选否
5. 适用机器类型选择编译环境（Linux）

## 插件使用
使用本插件的前置步骤，需要先将codecc代码扫描的产物使用`Download artifacts`下载当前workspace下
`Download artifacts`插件path字段配置为`*.json`，local path表示将产物`*.json`下载当前workspace下的具体路径，通常可以配置为`./${BK_CI_BUILD_ID}/`, 表示将产物下载到当前workspace下的`${BK_CI_BUILD_ID}`目录下

本插件的local path字段表示`*.json`文件所处的路径，需和`Download artifacts`插件local path字段保持一致
本插件会输出三个变量：
`total_serious`: 表示代码严重问题数量
`total_normal`:  表示代码一般问题数量
`total_prompt`:  表示代码提示问题数量