import streamlit as st
import time

# 1. 页面基本配置
st.set_page_config(page_title="专属私厨点餐系统", layout="wide", page_icon="🍳")

# 2. 初始化全局状态（购物车和订单状态）
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

# 3. 菜单数据定义
menu_data = [
    {"id": 1, "name": "招牌红烧肉", "price": 58, "img": "images/hongshaorou.jpg", "desc": "肥而不腻，入口即化",
     "tag": "热销主菜"},
    {"id": 2, "name": "孔雀开屏鱼", "price": 88, "img": "images/yu.jpg", "desc": "现杀活鱼，鲜美无比",
     "tag": "热销主菜"},
    {"id": 7, "name": "鲜香爆炒大虾", "price": 68, "img": "images/daxia.jpg", "desc": "Q弹爽滑，香辣过瘾",
     "tag": "热销主菜"},
    {"id": 5, "name": "滑嫩清蒸鸡蛋", "price": 15, "img": "images/jidan.jpg", "desc": "口感细腻，老少皆宜",
     "tag": "清爽素菜"},
    {"id": 6, "name": "爽脆炒黄芽菜", "price": 12, "img": "images/baicai.jpg", "desc": "清甜入味，大火快炒",
     "tag": "清爽素菜"},
    {"id": 3, "name": "清爽拍黄瓜", "price": 18, "img": "images/huanggua.jpg", "desc": "开胃解腻必备",
     "tag": "清爽素菜"},
    {"id": 4, "name": "五常大米饭", "price": 2, "img": "images/mifan.jpg", "desc": "软糯香甜", "tag": "主食"},
]


# 4. 定义菜单展示函数（已修复重复 Key 报错）
def show_menu_grid(items, tab_name):
    cols = st.columns(2)
    for index, item in enumerate(items):
        with cols[index % 2]:
            with st.container(border=True):
                # 图片展示
                try:
                    st.image(item['img'], use_container_width=True)
                except:
                    st.warning(f"🍱 图片制作中: {item['name']}")

                # 标题与价格
                c1, c2 = st.columns([3, 1])
                c1.subheader(item['name'])
                c2.subheader(f"￥{item['price']}")
                st.caption(item['desc'])

                # 【关键修复】：给按钮 Key 加上 tab_name 前缀，避免重复
                button_key = f"btn_{item['id']}_{tab_name}"
                if st.button(f"🛒 加入购物车", key=button_key, use_container_width=True):
                    st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                    st.toast(f"已将 {item['name']} 放入碗里~")


# --- 侧边栏布局 ---
with st.sidebar:
    try:
        # 这里请确保 images 文件夹里有这张图，或者换成你喜欢的照片
        st.image("images/gift.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>专属私厨点餐</h2>", unsafe_allow_html=True)
    except:
        st.title("🎁 爱的点餐机")

    st.divider()
    st.subheader("🛒 已选菜品")

    total_price = 0
    if not st.session_state.cart:
        st.info("快去挑选喜欢的菜吧~")
    else:
        for item_id, count in st.session_state.cart.items():
            dish = next(i for i in menu_data if i['id'] == item_id)
            st.write(f"**{dish['name']}** x {count}  — `￥{dish['price'] * count}`")
            total_price += dish['price'] * count

        st.divider()
        st.metric("合计金额", f"￥{total_price}")

        col_clear, col_ok = st.columns(2)
        if col_clear.button("清空", use_container_width=True):
            st.session_state.cart = {}
            st.session_state.order_submitted = False
            st.rerun()

        if col_ok.button("确认下单", type="primary", use_container_width=True):
            st.session_state.order_submitted = True

# --- 主界面布局 ---
st.title("👨‍🍳 今天想吃点什么？")

# 如果点击了下单，显示进度条动画
if st.session_state.order_submitted:
    st.balloons()
    st.success("订单已收到！正在为您全力烹饪中...")
    progress_bar = st.progress(0)
    status_text = st.empty()

    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
        if percent_complete < 30:
            status_text.text("正在精选食材... 🥬")
        elif percent_complete < 70:
            status_text.text("大火翻炒中，香味溢出... 🔥")
        else:
            status_text.text("正在精美摆盘... ✨")
    st.success("🎉 菜品已备齐，请享用！")
    # 延迟一会重置状态，让结果停留一下
    time.sleep(2)
    st.session_state.order_submitted = False

# 正常菜单分类展示
tab1, tab2, tab3 = st.tabs(["🏠 全部菜品", "🔥 热销主菜", "🥬 清爽素菜"])

with tab1:
    show_menu_grid(menu_data, "all")

with tab2:
    main_dishes = [i for i in menu_data if i['tag'] == "热销主菜"]
    show_menu_grid(main_dishes, "main")

with tab3:
    veggie_dishes = [i for i in menu_data if i['tag'] == "清爽素菜"]
    show_menu_grid(veggie_dishes, "veggie")

# --- 管理员后台 ---
st.write("")
st.write("")
st.divider()
with st.expander("🛠 管理员后台（后厨实时清单）"):
    if not st.session_state.cart:
        st.write("暂无待处理订单。")
    else:
        st.write("📋 **待出菜详情：**")
        order_summary = ""
        for item_id, count in st.session_state.cart.items():
            dish = next(i for i in menu_data if i['id'] == item_id)
            order_summary += f"【待做】{dish['name']} —— 数量：{count}\n"
        st.code(order_summary)