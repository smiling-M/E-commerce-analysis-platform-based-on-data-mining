from pyecharts.globals import CurrentConfig, NotebookType
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
import pandas as pd 
from pyecharts import options as opts
from sqlalchemy import create_engine 
from pyecharts.charts import Bar
import pymysql
import matplotlib.pyplot as plt
import main
def item_analysis(keyword):
    # 2.初始化数据库连接（按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名）
    engine = create_engine('mysql+pymysql://root:ml20sm2shiyao@localhost:3306/final_project')
    # 1.使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    sql_query = 'select * from %s;'%keyword # sql查询语句
    # 2.执行查询操作，并存入dataframe
    query_result = pd.read_sql_query(sql_query,engine) 
    web_df = query_result
    #选取在页面中多次（大于一次）出现的商店,并进行可视化
    df_count = pd.DataFrame(web_df['store_name'].value_counts())
    df_count.columns = ['count']
    bar = Bar(init_opts=opts.InitOpts(width="900px",height="450px"))
    df_count = df_count[df_count['count']!=1]
    count = df_count['count'].tolist()
    name = df_count.index.tolist()
    bar.add_yaxis("store count",count)
    bar.add_xaxis(name)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=keyword, subtitle="store count")
    )
    bar.render("static\charts\store_count.html")
    #销量
    bar = Bar(init_opts=opts.InitOpts(width="900px",height="450px"))
    sold_df = web_df.sort_values("sold",ascending=False)
    name = sold_df['item_name'].iloc[0:10].tolist()
    sold = sold_df['sold'].iloc[0:10].tolist()
    #print(sold_df.head())
    #print(name)
    bar.add_yaxis("sold",sold)
    bar.add_xaxis(name)
    #bar.reversal_axis()
    bar.set_global_opts(
        xaxis_opts = opts.AxisOpts(name_rotate=60,axislabel_opts={"rotate":45},is_show=False),
        title_opts=opts.TitleOpts(title=keyword, subtitle="sold")
        
    )
    
    bar.render("static\charts\sold.html")
    #好评率
    bar = Bar(init_opts=opts.InitOpts(width="900px",height="450px"))
    star_df = web_df.sort_values("star",ascending=False)
    name = star_df['item_name'].iloc[0:10].tolist()
    star = star_df['star'].iloc[0:10].tolist()
    bar.add_yaxis("star",star)
    bar.add_xaxis(name)
    bar.set_global_opts(
        xaxis_opts = opts.AxisOpts(name_rotate=60,axislabel_opts={"rotate":45},is_show=False),
        title_opts = opts.TitleOpts(title=keyword, subtitle="star")
        
    )
    bar.render("static\charts\star.html")
    #价格
    bar = Bar(init_opts=opts.InitOpts(width="900px",height="450px"))
    price_df = web_df.sort_values("price")
    name = price_df['item_name'].iloc[0:10].tolist()
    price = price_df['price'].iloc[0:10].tolist()
    bar.add_yaxis("price",price)
    bar.add_xaxis(name)
    bar.set_global_opts(
        xaxis_opts = opts.AxisOpts(is_show=False),
        title_opts = opts.TitleOpts(title=keyword, subtitle="price")
    )
    #print(price_df)
    bar.render("static\charts\price.html")
    #价格分布情况
    name = web_df['item_name'].tolist()
    price = web_df['price'].tolist()
    bar.add_yaxis("price",price)
    bar.add_xaxis(name)
    bar.set_global_opts(
        xaxis_opts = opts.AxisOpts(is_show=False),
        title_opts=opts.TitleOpts(title=keyword, subtitle="price distribution")
    )
    mean = web_df['price'].mean()
    bar.set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(y=mean,name='average') #显示平均值
            ],
            linestyle_opts=opts.LineStyleOpts(width = 3,color = '#FFFF00')  
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='min',name='minimum'),
                opts.MarkPointItem(type_='max',name='maximum'),
            ]
        ),
    )
    bar.render("static\charts\price_distribution.html")
    #价格和商品数量之间的关系
    bar = Bar(init_opts=opts.InitOpts(width="900px",height="450px"))
    price_df = web_df.sort_values("price")
    price = price_df['price'].tolist()
    sold = price_df['sold'].tolist()
    bar.add_xaxis(price)
    bar.add_yaxis("sold",sold,category_gap=0)
    bar.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=keyword, subtitle="price-sold")
    )
    bar.render("static\charts\price_sold.html")