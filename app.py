import streamlit as st
import pandas as pd
import datetime
import os
import time

# --- 1. 页面基本配置 ---
st.set_page_config(page_title="CIQ专属点餐系统", layout="wide", page_icon="🍳")

# --- 2. 初始化全局状态 ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False


# --- 3. 数据处理函数 ---
def save_order_to_csv(cart_items, total_price):
    """将订单记录到本地 CSV 文件中"""
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dish_details = ""
    for item_id, count in cart_items.items():
        dish = next(i for i in menu_data if i['id'] == item_id)
        dish_details += f"{dish['name']}x{count}; "

    new_data = {
        "下单时间": [order_time],
        "菜品详情": [dish_details],
        "总金额": [f"￥{total_price}"]
    }
    df_new = pd.DataFrame(new_data)

    file_path = "orders.csv"
    # 如果文件不存在则创建，存在则追加
    if not os.path.isfile(file_path):
        df_new.to_csv(file_path, index=False, encoding="utf_8_sig")
    else:
        df_new.to_csv(file_path, mode='a', header=False, index=False, encoding="utf_8_sig")


# --- 4. 菜单数据定义 ---
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


# --- 5. 菜单展示组件 ---
def show_menu_grid(items, tab_name):
    cols = st.columns(2)
    for index, item in enumerate(items):
        with cols[index % 2]:
            with st.container(border=True):
                try:
                    st.image(item['img'], use_container_width=True)
                except:
                    st.warning(f"🍱 图片制作中: {item['name']}")

                c1, c2 = st.columns([3, 1])
                c1.subheader(item['name'])
                c2.subheader(f"￥{item['price']}")
                st.caption(item['desc'])

                # 修复 Duplicate Key 报错
                button_key = f"btn_{item['id']}_{tab_name}"
                if st.button(f"🛒 加入购物车", key=button_key, use_container_width=True):
                    st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                    st.toast(f"已将 {item['name']} 放入购物车~")


# --- 6. 侧边栏布局 ---
with st.sidebar:
    try:
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
            if st.session_state.cart:
                # 下单时保存到 CSV
                save_order_to_csv(st.session_state.cart, total_price)
                st.session_state.order_submitted = True
            else:
                st.warning("请先点菜哦！")

# --- 7. 主界面逻辑 ---
st.title("👨‍🍳 今天想吃点什么？")

# 下单后的动画反馈
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
    time.sleep(2)
    st.session_state.order_submitted = False
    st.session_state.cart = {}  # 下单完清空购物车
    st.rerun()

# 分类展示标签页
tab1, tab2, tab3 = st.tabs(["🏠 全部菜品", "🔥 热销主菜", "🥬 清爽素菜"])
with tab1: show_menu_grid(menu_data, "all")
with tab2: show_menu_grid([i for i in menu_data if i['tag'] == "热销主菜"], "main")
with tab3: show_menu_grid([i for i in menu_data if i['tag'] == "清爽素菜"], "veggie")

# --- 8. 管理员后台 ---
st.write("")
st.divider()
with st.expander("🛠 管理员后台（历史订单查询）"):
    if os.path.exists("orders.csv"):
        df_history = pd.read_csv("orders.csv")
        st.write("📈 **最新订单流水：**")
        st.dataframe(df_history, use_container_width=True)

        st.download_button(
            label="下载订单报表",
            data=df_history.to_csv(index=False).encode('utf_8_sig'),
            file_name=f"orders_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.write("暂无历史订单记录。")