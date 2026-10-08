# 导入Chroma模块用于构建向量数据库
from langchain_chroma import Chroma

# 导入HuggingFaceEmbeddings用于加载embedding模型
from langchain_huggingface import HuggingFaceEmbeddings

# 指定本地embedding模型的路径
model_path = (
    "C:/Users/rensh/.cache/modelscope/hub/models/sentence-transformers/all-MiniLM-L6-v2"
)

# 加载指定路径的模型，并指定运行在CPU上
embeddings = HuggingFaceEmbeddings(
    model_name=model_path, model_kwargs={"device": "cpu"}
)

# 创建Chroma向量存储，指定持久化目录、embedding函数、集合名称和集合元数据
store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
    collection_name="kb_0b1c511d85224b488a5296c36eff8ae8",
    # collection_metadata={"hnsw:space": "cosine"},
)

# 定义检索的查询文本
query = "什么是青瓷梦?"

# 定义返回的top_k相似结果数量
top_k = 10

# 调用相似性搜索方法，返回结果及其分数
results = store.similarity_search_with_score(query, k=top_k)

# 获取当前集合的空间类型（如余弦、欧式等），默认为'cosine'
space = store._collection.configuration.get("hnsw").get("space", "cosine")

# 打印查询内容
print(f"查询: '{query}'")

# 提示分数的含义，分数越小越相似
print(f"分数解释: 值越小越相似")

# 遍历结果，逐条输出内容及分数解释
for i, (doc, score) in enumerate(results):
    # 根据空间类型选择分数的解释方式
    if space == "cosine":
        # 余弦空间：1-score即为相似度
        similarity = 1 - score
        interpretation = f"相似度: {similarity:.3f}"
    elif space == "ip":
        # 内积空间：取负数为相似度
        similarity = -score
        interpretation = f"内积: {similarity:.3f}"
    else:  # l2
        # 欧式距离直接显示
        interpretation = f"欧几里得距离: {score:.3f}"
    # 打印结果序号
    print(f"结果 {i+1}:")
    # 打印分数和解释
    print(f"  分数: {score:.4f} ({interpretation})")
    # 打印相应文档的前60个字符内容
    print(f"  内容: {doc.page_content[:60]}...")
    print()

# 给出距离/相似度的阈值建议说明
print("=== 阈值建议 ===")
if space == "cosine":
    # 针对余弦距离，输出典型阈值区间
    print("余弦距离阈值建议:")
    print("  <0.3 : 高度相关")
    print("  0.3-0.5 : 相关")
    print("  0.5-0.7 : 弱相关")
    print("  >0.7 : 可能不相关")
elif space == "l2":
    # 针对欧式距离，说明阈值依赖实际数据
    print("L2距离: 阈值依赖向量维度和数据分布")
