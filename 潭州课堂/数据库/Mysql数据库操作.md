#### **Mysql 库基础命令**

```
mysql -u用户名 -p密码 # 进入
exit # 退出
show databases; # 查看数据库列表
create database if not exists test; # 创建数据库 if not exists 检查是否重复
drop database if exists test; # 删除数据库 if exists 检查是否有此库
use 库名; # 进入库
select database(); # 查看当前所在库
drop database 库名 # 删除库
```

#### **Mysql 表基础命令**

```
show tables; # 查看表
create table if not exists 表名(字段 类型，字段 类型，...)； # 创建表 
show create table 表名; # 显示表详细信息
drop table 表名; # 删除表
```

#### **Mysql 数据操作命令**

```
# 增
insert into 表名 values (字段 值，字段 值，...); # 全字段插入
insert into 表名(字段) values(字段值); # 指定字段插入
insert into 表名(字段) values(字段值)，（字段值）,....; # 多行插入
# 查
select * from 表名； # 全字段查询
select 字段，字段，... from 表名； # 指定字段查询
select 字段 from 表名 where 条件； # 条件查询
# 查
update 表名 set 字段=新值； # 修改所有数据
uodate 表名 set 字段1=新值，字段2=新值，... # 修改多个字段值
update 表名 set 字段=新值 where 条件； # 修改满足条件数据
# 删
delete from 表名； # 删除表中所有数据
delete from 表名 where 条件； # 删除满足条件的数据
```

#### **Mysql 常用数值类型**

|     **类型**     | **大小**                                     | **范围（有符号）**                                           | **范围（无符号）**                                           | **用途**            |
| :--------------: | -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------- |
|   **TINYINT**    | **1 字节**                                   | **(-128，127)**                                              | **(0，255)**                                                 | **小整数值**        |
|   **SMALLINT**   | **2 字节**                                   | **(-32 768，32 767)**                                        | **(0，65 535)**                                              | **大整数值**        |
|  **MEDIUMINT**   | **3 字节**                                   | **(-8 388 608，8 388 607)**                                  | **(0，16 777 215)**                                          | **大整数值**        |
| **INT或INTEGER** | **4 字节**                                   | **(-2 147 483 648，2 147 483 647)**                          | **(0，4 294 967 295)**                                       | **大整数值**        |
|    **BIGINT**    | **8 字节**                                   | **(-9 233 372 036 854 775 808，9 223 372 036 854 775 807)**  | **(0，18 446 744 073 709 551 615)**                          | **极大整数值**      |
|    **FLOAT**     | **4 字节**                                   | **(-3.402 823 466 E+38，1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38)** | **0，(1.175 494 351 E-38，3.402 823 466 E+38)**              | **单精度 浮点数值** |
|    **DOUBLE**    | **8 字节**                                   | **(1.797 693 134 862 315 7 E+308，2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308)** | **0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308)** | **双精度 浮点数值** |
|   **DECIMAL**    | **对DECIMAL(M,D) ，如果M>D，为M+2否则为D+2** | **依赖于M和D的值**                                           | **依赖于M和D的值**                                           | **小数值**          |

#### **Mysql 常用字符类型**

|      类型      |          特性           |                用途                 |
| :------------: | :---------------------: | :---------------------------------: |
|    **CHAR**    |      **0-255字节**      |           **定长字符串**            |
|  **VARCHAR**   |      **0-255字节**      |           **变长字符串**            |
|  **TINYBLOB**  |      **0-255字节**      | **不超过 255 个字符的二进制字符串** |
|  **TINYTEXT**  |      **0-255字节**      |          **短文本字符串**           |
|    **BLOB**    |    **0-65 535字节**     |     **二进制形式的长文本数据**      |
|    **TEXT**    |    **0-65 535字节**     |           **长文本数据**            |
| **MEDIUMBLOB** |  **0-16 777 215字节**   |  **二进制形式的中等长度文本数据**   |
| **MEDIUMTEXT** |  **0-16 777 215字节**   |        **中等长度文本数据**         |
| **LOGNGBLOB**  | **0-4 294 967 295字节** |    **二进制形式的极大文本数据**     |
|  **LONGTEXT**  | **0-4 294 967 295字节** |          **极大文本数据**           |

#### **Mysql 枚举集合**

| **类型** | **大小(字节)** | **最多成员数** |
| :------: | :------------: | :------------: |
|   ENUM   |       64       |     65535      |
|   SET    |       64       |       64       |

#### **Mysql 时间类型**

|   **类型**    | **大小(字节)** |                  **范围**                   |        **格式**         |           **用途**           |
| :-----------: | :------------: | :-----------------------------------------: | :---------------------: | :--------------------------: |
|   **DATE**    |     **3**      |          **1000-01-01/9999-12-31**          |     **YYYY-MM-DD**      |          **日期值**          |
|   **TIME**    |     **3**      |        **'-838:59:59'/'838:59:59'**         |      **HH:MM:SS**       |     **时间值或持续时间**     |
|   **YEAR**    |     **1**      |                **1901/2155**                |        **YYYY**         |          **年份值**          |
| **DATETIME**  |     **8**      | **1000-01-01 00:00:00/9999-12-31 23:59:59** | **YYYY-MM-DD HH:MM:SS** |     **混合日期和时间值**     |
| **TIMESTAMP** |     **8**      |     **1970-01-01 00:00:00/2037 年某时**     |   **YYYYMMDD HHMMSS**   | **混合日期和时间值，时间戳** |

#### **Mysql linux系统SQL脚本导入**

```
mysql -h localhost -u root -p 路径
mysql -u root -p # 进入数据库
mysql>use 数据库
然后使用source命令，后面参数为脚本文件(如这里用到的.sql)
mysql>source /home/pt/test.sql
```

#### **Mysql 筛选条件**

```
# 排序  
select * from 表名 order by 字段； # 默认asc 正序， desc倒序
# 限制
select * from 表名 limit 条数；
select * from 表名 limit 开始位置，条数； 从索引位置开始显示多少条
# 去重
select distinct 字段 from 表名；
# 模糊查询 like 
	% 代替任意多个字符
	_ 代替任意一个字符	
# 范围查询
select * from 表名 between 条件1 and 条件2；连续范围
select * from 表名 字段 in（条件1，条件2，...）； 范围查询 只要满足其中条件就返回

```

#### **Mysql  聚合分组**

```
# 聚合函数
	select 函数（字段） form 表名；
	常用函数
	count（） 统计个数
	sum（） 求和
	max（）最大值
	avg（）平均值
	min（）最小值
	gtoup_concat（） 列出字段全部值
# 分组查询 group by
	select 字段，聚合函数（*） from 表 group by 字段；
# 聚合筛选 having
	select 字段1 from 表 group by 字段1， 字段2 having 字段2条件； 用字段2的条件限制字段1的输出结果

条件判断执行优先级  where > 聚合函数和别名 > having
```

#### **Mysql 子查询（嵌套查询）**

```
# 使用条件
	1.嵌套在查询内部
	2.必须在（）内使用
select * from 表 where age >（select avg（age）from students） 
```

#### **Mysql 连接查询**

```
# 无条件内连接  表1的每一项和表2每一项依次组合
	select * from 表1 join 表2；
	
# 有条件内连接  on 条件
	select * from 表1 join 表2 on 条件；
	
# 外连接
	左外连接 以左表为基准 left
	右外连接 以右表为基准 right
	
# 多表联合查询
select count(*) from (select * from 表1 where 表1字段 = (select 表2字段 from 表2 where 表2条件))as a left join 表3 on a.student_number=students.number where age>18;

select * from 表1 where 表1字段 = (select 表2字段 from 表2 where 表2条件）
#以表2返回的结果为条件查询表1，然后整个条件结果重命名为a 和 表三连接查询 得到想要结果 

```

#### **Mysql 表结构修改（alter）**

```
alter table 表名 rename to 新表名；  # 修改表名
alter table 表名 change name 字段名 新字段名 数据类型； # 修改字段名
alter table 表名 modify 字段名 数据类型； # 修改字段类型
alter table 表名 add 字段名 数据类型；  添加字段
alter table 表名 drop 字段名； # 删除字段
```

#### **Mysql 约束条件（主键、外键）**

```
# 默认 default
	create table 表 （id int defult 100,name varchar(10)） 
	# 创建表时字段指定一个默认参数，添加数据时如不添加此参数将使用默认参数
	
# 非空 not null
	create table 表 （id int not null,name varchar(10)）
	
# 唯一 nuique key
	create table 表 （id int unique key,name varchar(10)）
	# 只能有一个
	
# 自增长 auto_increment 
	create table 表 （id int primary key auto_increment,name varchar(10)）auto_increment=100
	# 设置id 为主键 且自增长 指定默认值为100 从100开始
	
# 主键 primary key 唯一而且非空 如不指定会自动设置一个
	create table 表 （id int primary key,name varchar(10)）
	
# 外键 foreign key
	create table b表（b_id int primary key,b_name varshar(20) not null,fy_id not null, 
	foreign key(fy_id) references a表(a_id)） # 设置外键
```

#### **Mysql 表关系**

```
# 一对一
# 一对多
# 多对多
create table 中间表（a_id，b_id,primary key（a_id,b_id）,  # primary key（a_id,b_id） 设置联合主键
				foreign key(a_id) regerences A(a_id),  # a_id 外键关联 A表a_id
				foreign key(b_id) regerences B(b_id)）;  # b_id 外键关联 B表b_id
				
```