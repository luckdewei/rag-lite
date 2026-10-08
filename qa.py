"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
import uuid

# 创建统一的Base类，所有的ORM模型都应该继承此Base类
Base = declarative_base()


# 定义所有的模型的基类
class BaseModel(Base):
    # 把此类标准为抽象类，这样就不会创建表了
    __abstract__ = True

    # 把模型对象转成python字典的方法
    def to_dict(self, exclude, **kwargs):
        # 要排除的字段列表 ["password_hash"]
        exclude = exclude or []
        result = {}
        # 获取当模型类的所有的列定义
        mapper = inspect(self.__class__)
        # 遍历所有的列
        for column in mapper.columns:
            # 获取列名
            col_name = column.name
            if col_name in exclude:
                continue
            # 获取此字段名的值
            value = getattr(self, col_name, None)
            # 如果value有是日期类型的话，调用isoformat转换为字符串
            if hasattr(value, "isoformat"):
                result[col_name] = value.isoformat() if value else None
            else:
                result[col_name] = value
        return result

    def __repr__(self):
        # 如果子类指定义__repr_fields__值，优先显示这些字段
        if hasattr(self, "__repr_fields__"):
            fields = getattr(self, "__repr_fields__")
            attrs = ", ".join(f"{field}={getattr(self,field,None)}" for field in fields)
        else:
            attrs = f"id={getattr(self,'id',None)}"
        return f"<{self.__class__.__name__}({attrs})>"


class User(BaseModel):
    # 指定数据库表名为user
    __tablename__ = "user"
    # 指定__repr__显示的字段
    __repr_fields__ = ["id", "username"]
    id = Column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:32])
    # 用户名
    username = Column(String(64), nullable=False, unique=True, index=True)
    # username: Mapped[str] = mapped_column(String(100), nullable=False)
    # 邮箱
    email = Column(String(128), nullable=True, unique=True, index=True)
    # 密码哈希字符
    password_hash = Column(String(255), nullable=False)
    # 是否激活 默认为激活 不可为空
    is_active = Column(Boolean, nullable=False, default=True)
    # 创建时间 默认为当前时间 创建索引
    created_at = Column(DateTime, default=func.now(), index=True)
    # 更新时间 默认为当前时间，在数据更新的自动更新为当前最新的时间
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self, include_password=False, **kwargs):
        exclude = ["password_hash"] if not include_password else []
        return super().to_dict(exclude=exclude, **kwargs)


user1 = User(
    username="zhangsan",
    email="zhangsan@qq.com",
    password_hash="password_hash",
    is_active=True,
)
print(user1.id)
user2 = User(
    id="myid",
    username="zhangsan",
    email="zhangsan@qq.com",
    password_hash="password_hash",
    is_active=True,
)
print(user2.id)


import os

cover_image_filename = "gigi.jpg"
file_ext_with_dot = os.path.splitext(cover_image_filename)[1].lower()
print(file_ext_with_dot)

# mimetypes 3.14
# filetype 3.13
import filetype

kind = filetype.guess("1.png")
print(kind.mime)
print(kind.extension)


"""

import os


filename = "123.456.789.jpg"


def splitext(filename):
    if not filename:
        return "", ""
    # 查找最后一个点的位置
    dot_inex = filename.rfind(".")
    if dot_inex <= 0:
        return filename, ""
    root = filename[:dot_inex]
    ext = filename[dot_inex:]
    return root, ext


print(splitext(filename))


# 在本项目中我们有3个Document
# 第一个来自  from langchain_core.documents import Document  import Document 代表一个文档，里面有page_content文档内容
# 另一个是来自于我们自己写的sqlalchemy模型类 from app.models.document import Document
# 一会还有一个chromadb里面也有Document


# langchain的Document就叫Document
# 自己写的Document改名为 DocumentModel
# chromadb的Document改名为 DocumentVector


# 一个知识库 有多个文档，一个知识库对应一个 collection
# 一个知识库对应多个文档，每个文件对应一个文件
# 当我们在插入的时候插入什么，那么在删除的时候就要删除什么
# 1. 上传一个文件storages\documents\abb6abf92d954f65b5a210733dd2d5f8\813fbfeaf47b4effa0368669d5f2f30f\三国演义.pdf
# 2. 向document表中插入了一条数据
# 3. 向向量数据库中插入了多条文档


# vector_service.delete_documents(
#    collection_name=collection_name, filter={"doc_id": doc_id}
# )


# 理解：新增知识库，一个知识库可以上传多个文档，
# #处理某个文档就是把文档分块向量化存储到向量数据库的过程；
# 文件库存放上传的文档，路径是知识库id/文档id/文件名；
# MySQL 数据库的 documents 表存储文档元数据；向量数据库存储分块信息以及文档分块向量


# 在本项目中我们有3个Session

# Flask框架一个Session,它表示客户端在服务器存放的数据,当客户端登录后会,服务器会向客户端种植一个cookie,在服务器对应一个会话对象,以保存用户登录状态
# ChatSession 中一个sqlalchemy模型,对应着数据库里的会话表,存放对话的历史消息
# session 是连接 数据库的连接session,通过它可以操作数据库


# 所有hnsw:space设置下，similarity_search_with_score返回的score都是距离值（distance），不是相似度（similarity）。
# l2 ip consine  score都是越小越相似

import numpy as np

scores = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
max_score = float(np.max(scores)) if len(scores) > 0 and np.max(scores) > 0 else 1.0
print(max_score)
# 归一化BM25分数 [1,2,3,4,5]  /5 = [0.2,,,,1]
normalized_scores = scores / max_score if max_score > 0 else scores
print(normalized_scores)


# doc就是chroma数据库返回的文档，我们在处理过程不断的向它的metadtata中插入新的元数据
# retrieval_type 检索类型 vector keyword hybrid rerank
# rerank_score  重排序分数
# vector_score 向量分数
# keywrod_score 关键字分数 全文检索分数 BM25分数
# rrf_score 融合检索分数

#  重排序是按照什么重新排序 使用的是重排序模型实现的
