---
title: Fortran netCDF library安装记
tags: [Fortran]
category: 技术探索
date: 2014-12-10 18:32:00
---

帮一个朋友安装国内某名校某人写的一个fortran程序

此程序主要用到了netcdf库.

最开始运行make，报undefined reference to `netcdf_mp_nf90_get_att_one_fourbytereal_'之类的错，经网上一顿搜索，问题定位在fortran编译器没有链接到netCDF Fortran库..

查看Makefile，加上-lnetcdff，报没有libnetcdff.so..

开始艰难的编译Fortran netCDF library..

IBM CRL的网络一如既往的不给力..幸好的是..其中的yellowzone区域的网络还是很给力的的..

安装Fortran netCDF library需要C netCDF library，安装C netCDF library的过程中又缺少了hdf5库..

下载hdf5源码包..安装..

之前有安装过C netCDF library，除了make check了一晚上还没结束..一切还是比较顺利的..

安装Fortran netCDF library是比较痛苦的，中间几乎有想放弃的时候.

1.系统自带的fortran编译器gfortran版本过低，configure的时候就一直出问题,换成了gfortran44..

2.用gfortran44配置时，同时需要设置环境变量CC，指向之前编译C库的C编译器，如/usr/bin/gcc..

3.configure通过，但make时一直报莫名奇妙的错误,DHAVE_CONFIG_H: Command not found或者g: Command not found..经过一阵煎熬..折腾..把gfortran44 mv到gfortran(之前用gfrtran44编译是设置的环境变量FC)，勉强make成功..

4.这下有了libnetcdff.so，但仍然报undefined reference to `netcdf_mp_nf90_get_att_one_fourbytereal_'，用nm命令查看libnetcdff.so，只发现了netcdf_MOD_nf90_get_att_one_fourbytereal..改变Makefile脚本，设置FC为gfortran(之前是mpif90 -f90=ifort)，但出现了其他的错..考虑用ifort编译Fortran netCDF..编译成功..并把FC设置为ifort..make成功...