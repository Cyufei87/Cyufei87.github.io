---
title: 从ftp服务器上下载文件或文件夹
tags: [FTP]
category: 技术探索
date: 2016-12-14 17:32:36
---

`
def download_paths(ftp_object, path, destination):
    """
    从ftp服务器上下载文件或文件夹
    :param ftp_object: 一个已连接的ftplib.FTP对象
    :param path: ftp上的路径
    :param destination: 本地文件夹
    """
    to_path = os.path.join(destination, os.path.basename(path))

    file_list = ftp_object.nlst(path)
    if len(file_list) == 1 and file_list[0] == path:  # 如果是文件
        ftp_object.retrbinary("RETR " + path, open(to_path, "wb").write)
    elif len(file_list) > 0:
        if not os.path.exists(to_path):
            os.makedirs(to_path)
        for f in file_list:
            download_paths(ftp_object, f, to_path)
`