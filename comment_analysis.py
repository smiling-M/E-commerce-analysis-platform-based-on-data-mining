# %%
#from pyecharts.globals import CurrentConfig, NotebookType
#CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
import pandas as pd 
#from pyecharts import options as opts
from sqlalchemy import create_engine 
#from pyecharts.charts import Bar
import pymysql
#import matplotlib.pyplot as plt
# import item_crawler
import comment_crawler
import re
import pyLDAvis.gensim_models
import spacy
import itertools
import matplotlib.pyplot as plt
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import nltk#添加英语单词语料库，将不是英语单词的词删除
from nltk.corpus import words
from gensim import corpora, models
from pyecharts.charts import WordCloud


# %%
def wordcloud(product_id):
    # 2.初始化数据库连接（按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名）
    engine = create_engine('mysql+pymysql://root:ml20sm2shiyao@localhost:3306/final_project')
    # 1.使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    keyword = product_id
    sql_query = 'select * from comment_%s;'%keyword # sql查询语句
    # 2.执行查询操作，并存入dataframe
    comment_df = pd.read_sql_query(sql_query,engine) 
    # # %%
    # comment_df.head()

    # # %%
    # comment_df.shape

    # # %%
    # #统计重复数据
    # comment_df[['comment_type','comment']].duplicated().sum()
    #评论去重
    comment_df = comment_df.drop_duplicates(subset=['comment_type','comment'])

    #数据清洗
    pattern = re.compile('[^a-zA-Z0-9]|[Ss]o|[Vv]ery|[Aa]nd')
    comment_df['comment'] = comment_df['comment'].apply(lambda x : pattern.sub(' ',x))
    pattern1 = re.compile('  39 ')
    comment_df['comment'] = comment_df['comment'].apply(lambda x : pattern1.sub('\'',x))
    # print(comment_df)
    pos_comment = comment_df
    neg_comment = comment_df
    pos_comment = pos_comment[pos_comment['comment_type']=='positive']
    neg_comment = neg_comment[neg_comment['comment_type']=='negetive']# %%
    #词性标注
    nlp = spacy.load("en_core_web_sm")
    result = pd.DataFrame(columns=['word', 'word_type', 'content_type'])
    # Find named entities, phrases and concepts
    # for entity in doc.ents:
    #     print(entity.text, entity.label_)
    def word_note(type):
        word_type = [token.lemma_ for token in doc if token.pos_ == type]
        i = 0
        while i<len(word_type):
            result.loc[len(result.index)] = [word_type[i], type, row['comment_type']]
            i+=1
    for index,row in comment_df.iterrows():
        doc = nlp(row['comment'])
        #result.loc[len(result.index)] = [value1, value2, value3, ...]
        word_note('NOUN')
        word_note('ADJ')
        word_note('ADV')#将正负面评价分开
    noun_result = result.loc[result['word_type'] == 'NOUN']
    pos_noun_result = noun_result.loc[noun_result['content_type']=='positive']
    neg_noun_result = noun_result.loc[noun_result['content_type']=='negetive']
    # print(pos_noun_result)
    pos_noun_count = pd.DataFrame(pos_noun_result['word'].value_counts())
    pos_noun_count.columns = ['count']
    pos_word = pos_noun_count.index.tolist()
    pos_count = pos_noun_count['count'].tolist()
    pos_noun_words = []
    for i in range(len(pos_noun_count)):
        if pos_word[i] in words.words():
            pos_noun_words.append((pos_word[i],int(pos_count[i])))
    print(pos_noun_words)
    neg_noun_count = pd.DataFrame(neg_noun_result['word'].value_counts())
    neg_noun_count.columns = ['count']
    neg_word = neg_noun_count.index.tolist()
    neg_count = neg_noun_count['count'].tolist()
    neg_noun_words = []
    for i in range(len(neg_noun_count)):
        if neg_word[i] in words.words():
            neg_noun_words.append((neg_word[i],int(neg_count[i])))
    print(neg_noun_words)
    #绘制词云
    
    w = (
        WordCloud()
        .add("", pos_noun_words, word_size_range=[12, 55],shape='circle')
        .set_global_opts(title_opts=opts.TitleOpts(title="positive wordcloud"))
        .render("static/charts/wordcloud_pos_noun.html")
    )
    w1 = (
        WordCloud()
        .add("", neg_noun_words, word_size_range=[12, 55],shape='circle')
        .set_global_opts(title_opts=opts.TitleOpts(title="negetive wordcloud"))
        .render("static/charts/wordcloud_neg_noun.html")
    )
   

    













# %%
def topic(product_id):
    # 2.初始化数据库连接（按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名）
    engine = create_engine('mysql+pymysql://root:ml20sm2shiyao@localhost:3306/final_project')
    # 1.使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    keyword = product_id
    sql_query = 'select * from comment_%s;'%keyword # sql查询语句
    # 2.执行查询操作，并存入dataframe
    comment_df = pd.read_sql_query(sql_query,engine) 
    # # %%
    # comment_df.head()

    # # %%
    # comment_df.shape

    # # %%
    # #统计重复数据
    # comment_df[['comment_type','comment']].duplicated().sum()
    #评论去重
    comment_df = comment_df.drop_duplicates(subset=['comment_type','comment'])

    #数据清洗
    pattern = re.compile('[^a-zA-Z0-9]|[Ss]o|[Vv]ery|[Aa]nd')
    comment_df['comment'] = comment_df['comment'].apply(lambda x : pattern.sub(' ',x))
    pattern1 = re.compile('  39 ')
    comment_df['comment'] = comment_df['comment'].apply(lambda x : pattern1.sub('\'',x))
    # print(comment_df)
    pos_comment = comment_df
    neg_comment = comment_df
    pos_comment = pos_comment[pos_comment['comment_type']=='positive']
    neg_comment = neg_comment[neg_comment['comment_type']=='negetive']# %%
    #词性标注
    nlp = spacy.load("en_core_web_sm")
    result = pd.DataFrame(columns=['word', 'word_type', 'content_type'])
    # Find named entities, phrases and concepts
    # for entity in doc.ents:
    #     print(entity.text, entity.label_)
    def word_note(type):
        word_type = [token.lemma_ for token in doc if token.pos_ == type]
        i = 0
        while i<len(word_type):
            result.loc[len(result.index)] = [word_type[i], type, row['comment_type']]
            i+=1
    for index,row in comment_df.iterrows():
        doc = nlp(row['comment'])
        #result.loc[len(result.index)] = [value1, value2, value3, ...]
        word_note('NOUN')
        word_note('ADJ')
        word_note('ADV')#将正负面评价分开
    noun_result = result.loc[result['word_type'] == 'NOUN']
    pos_noun_result = noun_result.loc[noun_result['content_type']=='positive']
    neg_noun_result = noun_result.loc[noun_result['content_type']=='negetive']
    # print(pos_noun_result)
    pos_noun_count = pd.DataFrame(pos_noun_result['word'].value_counts())
    pos_noun_count.columns = ['count']
    pos_word = pos_noun_count.index.tolist()
    pos_count = pos_noun_count['count'].tolist()
    pos_noun_words = []
    for i in range(len(pos_noun_count)):
        if pos_word[i] in words.words():
            pos_noun_words.append((pos_word[i],int(pos_count[i])))
    # print(pos_noun_words)
    neg_noun_count = pd.DataFrame(neg_noun_result['word'].value_counts())
    neg_noun_count.columns = ['count']
    neg_word = neg_noun_count.index.tolist()
    neg_count = neg_noun_count['count'].tolist()
    neg_noun_words = []
    for i in range(len(neg_noun_count)):
        if neg_word[i] in words.words():
            neg_noun_words.append((neg_word[i],int(neg_count[i])))
    # print(neg_noun_words)
    # 建立词典
    pos_dict = corpora.Dictionary([[i] for i in pos_noun_result['word']])  # positive
    neg_dict = corpora.Dictionary([[i] for i in neg_noun_result['word']])  # negetive

    # 建立语料库
    pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in pos_noun_result['word']]]  # 正面
    neg_corpus = [neg_dict.doc2bow(j) for j in [[i] for i in neg_noun_result['word']]]   # 负面
    # def cos(vector1, vector2):
    # # """
    # # 计算两个向量的余弦相似度函数
    # # :param vector1:
    # # :param vector2:
    # # :return: 返回两个向量的余弦相似度
    # # """
    #     dot_product = 0.0
    #     normA = 0.0
    #     normB = 0.0
    #     for a, b in zip(vector1, vector2):
    #         dot_product += a * b
    #         normA += a ** 2
    #         normB += b ** 2
    #     if normA == 0.0 or normB == 0.0:
    #         return (None)
    #     else:
    #         return (dot_product / ((normA * normB) ** 0.5))
    # def lda_k(x_corpus, x_dict):
    #     """
    #     主题数寻优
    #     :param x_corpus: 语料库
    #     :param x_dict: 词典
    #     :return:
    #     """
    #     # 初始化平均余弦相似度
    #     mean_similarity = []
    #     mean_similarity.append(1)

    #     # 循环生成主题并计算主题间相似度
    #     for i in np.arange(2, 11):
    #         lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练
    #         for j in np.arange(i):
    #             term = lda.show_topics(num_words=50)

    #         # 提取各主题词
    #         top_word = []
    #         for k in np.arange(i):
    #             top_word.append([''.join(re.findall('"(.*)"', i)) for i in term[k][1].split('+')])  # 列出所有词

    #         # 构造词频向量
    #         word = sum(top_word, [])  # 列出所有的词
    #         unique_word = set(word)  # 去除重复的词

    #         # 构造主题词列表，行表示主题号，列表示各主题词
    #         mat = []
    #         for j in np.arange(i):
    #             top_w = top_word[j]
    #             mat.append(tuple([top_w.count(k) for k in unique_word]))

    #         p = list(itertools.permutations(list(np.arange(i)), 2))
    #         l = len(p)
    #         top_similarity = [0]
    #         for w in np.arange(l):
    #             vector1 = mat[p[w][0]]
    #             vector2 = mat[p[w][1]]
    #             top_similarity.append(cos(vector1, vector2))

    #         # 计算平均余弦相似度
    #         mean_similarity.append(sum(top_similarity) / l)
    #     return (mean_similarity)
    # pos_k = lda_k(pos_corpus, pos_dict)
    # neg_k = lda_k(neg_corpus, neg_dict)        
    # print('正面评论主题的平均相似度',pos_k)
    # print('负面评论主题的平均相似度',neg_k)

    # 绘制主题平均余弦相似度图形
    # 解决中文显示问题
    plt.rcParams['font.sans-serif']=['SimHei']
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False  
    fig = plt.figure(figsize=(10,8))
    pos_lda = models.LdaModel(pos_corpus, num_topics = 3, id2word = pos_dict)  
    neg_lda = models.LdaModel(neg_corpus, num_topics = 3, id2word = neg_dict)  
    pos_lda.print_topics(num_words = 10)
    neg_lda.print_topics(num_words = 10)
    for topic in pos_lda.print_topics(num_words=10):
        termNumber = topic[0]
        print(topic[0], ':', sep='')
        listOfTerms = topic[1].split('+')
        for term in listOfTerms:
            listItems = term.split('*')
            print('  ', listItems[1], '(', listItems[0], ')', sep='')
    for topic in neg_lda.print_topics(num_words=10):
        termNumber = topic[0]
        print(topic[0], ':', sep='')
        listOfTerms = topic[1].split('+')
        for term in listOfTerms:
            listItems = term.split('*')
            print('  ', listItems[1], '(', listItems[0], ')', sep='')
    d = pyLDAvis.gensim_models.prepare(pos_lda, pos_corpus, pos_dict)
    e = pyLDAvis.gensim_models.prepare(neg_lda, neg_corpus, neg_dict)
    # pyLDAvis.show(d)
    # d = pyLDAvis.gensim.prepare(pos_lda, pos_corpus, pos_dict)
    pyLDAvis.save_html(d, 'static\charts\lda_pos.html')
    pyLDAvis.save_html(e, 'static\charts\lda_neg.html')